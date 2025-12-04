import os
import hashlib
from typing import List, Dict, Any
from decimal import Decimal
import httpx

from api.persistence.repositories.carteira_repository import CarteiraRepository
from api.models.carteira_models import Carteira, CarteiraCriada
from api.models.moeda_models import Saldo
from api.models.movimento_models import DepositoRequest, SaqueRequest, ConversaoRequest, TransferenciaRequest
from api.models.moeda_models import Saldo

class CarteiraService:
    def __init__(self, carteira_repo: CarteiraRepository):
        self.repo = carteira_repo
        self.TAXA_SAQUE = Decimal(os.getenv("TAXA_SAQUE_PERCENTUAL", "0.01"))
        self.TAXA_CONVERSAO = Decimal(os.getenv("TAXA_CONVERSAO_PERCENTUAL", "0.02"))
        self.TAXA_TRANSFERENCIA = Decimal(os.getenv("TAXA_TRANSFERENCIA_PERCENTUAL", "0.01"))

    def _validar_chave_privada(self, endereco: str, chave_privada: str) -> bool:
        hash_enviado = hashlib.sha256(chave_privada.encode()).hexdigest()
        hash_armazenado = self.repo.buscar_hash_privada(endereco)
        return hash_enviado == hash_armazenado

    def _buscar_id_moeda(self, codigo: str) -> int:
        id_moeda = self.repo.buscar_id_moeda_por_codigo(codigo)
        if not id_moeda:
            raise ValueError(f"Moeda com código {codigo} não suportada.")
        return id_moeda

    def criar_carteira(self) -> CarteiraCriada:
        row = self.repo.criar()
        return CarteiraCriada(
            endereco_carteira=row["endereco_carteira"],
            data_criacao=row["data_criacao"],
            status=row["status"],
            chave_privada=row["chave_privada"],
        )

    def buscar_por_endereco(self, endereco_carteira: str) -> Carteira:
        row = self.repo.buscar_por_endereco(endereco_carteira)
        if not row:
            raise ValueError("Carteira não encontrada")
        return Carteira(endereco_carteira=row["endereco_carteira"], data_criacao=row["data_criacao"], status=row["status"])

    def obter_saldos_por_endereco(self, endereco_carteira: str) -> List[Saldo]:
        if not self.repo.buscar_por_endereco(endereco_carteira):
            raise ValueError("Carteira não encontrada")
        
        rows = self.repo.listar_saldos_por_endereco(endereco_carteira)
        return [Saldo(codigo_moeda=r["codigo"], saldo=r["saldo"]) for r in rows]

    def obter_saldo_global(self) -> List[Saldo]:
        rows = self.repo.somar_saldo_global() 
        return [Saldo(codigo_moeda=r["codigo_moeda"], saldo=r["saldo_total"]) for r in rows]

    def listar(self) -> List[Carteira]:
        rows = self.repo.listar()
        return [Carteira(endereco_carteira=r["endereco_carteira"], data_criacao=r["data_criacao"], status=r["status"]) for r in rows]

    def bloquear(self, endereco_carteira: str) -> Carteira:
        row = self.repo.atualizar_status(endereco_carteira, "BLOQUEADA")
        if not row:
            raise ValueError("Carteira não encontrada")
        return Carteira(endereco_carteira=row["endereco_carteira"], data_criacao=row["data_criacao"], status=row["status"])

    def depositar(self, endereco_carteira: str, dados: DepositoRequest):
        id_moeda = self._buscar_id_moeda(dados.codigo_moeda)
        
        self.repo.atualizar_saldo(endereco_carteira, id_moeda, dados.valor)
        
        self.repo.registrar_movimento_simples(endereco_carteira, id_moeda, 'DEPOSITO', dados.valor, Decimal(0))
        return self.obter_saldos_por_endereco(endereco_carteira)

    def sacar(self, endereco_carteira: str, dados: SaqueRequest):
        if not self._validar_chave_privada(endereco_carteira, dados.chave_privada):
            raise ValueError("Chave privada inválida.")

        id_moeda = self._buscar_id_moeda(dados.codigo_moeda)
        saldo_atual = self.repo.buscar_saldo(endereco_carteira, id_moeda)
        
        taxa_valor = dados.valor * self.TAXA_SAQUE
        valor_total_debito = dados.valor + taxa_valor
        
        if saldo_atual < valor_total_debito:
            raise ValueError("Saldo insuficiente para saque + taxa.")

        self.repo.atualizar_saldo(endereco_carteira, id_moeda, -valor_total_debito)
        
        self.repo.registrar_movimento_simples(endereco_carteira, id_moeda, 'SAQUE', dados.valor, taxa_valor)
        return self.obter_saldos_por_endereco(endereco_carteira)

    async def _obter_cotacao_coinbase(self, moeda_origem: str, moeda_destino: str) -> Decimal:
        url = f"https://api.coinbase.com/v2/prices/{moeda_origem}-{moeda_destino}/spot"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return Decimal(data['data']['amount'])

    async def converter_moeda(self, endereco_carteira: str, dados: ConversaoRequest):
        if not self._validar_chave_privada(endereco_carteira, dados.chave_privada):
            raise ValueError("Chave privada inválida.")

        id_origem = self._buscar_id_moeda(dados.codigo_origem)
        id_destino = self._buscar_id_moeda(dados.codigo_destino)
        
        saldo_origem = self.repo.buscar_saldo(endereco_carteira, id_origem)
        
        taxa_valor_origem = dados.valor_origem * self.TAXA_CONVERSAO
        valor_total_debito = dados.valor_origem + taxa_valor_origem
        
        if saldo_origem < valor_total_debito:
            raise ValueError("Saldo insuficiente para conversão + taxa.")

        cotacao = await self._obter_cotacao_coinbase(dados.codigo_origem, dados.codigo_destino)
        
        valor_destino = dados.valor_origem * cotacao
        
        self.repo.atualizar_saldo(endereco_carteira, id_origem, -valor_total_debito)
        self.repo.atualizar_saldo(endereco_carteira, id_destino, valor_destino)

        self.repo.registrar_conversao_db({
            "endereco_carteira": endereco_carteira,
            "id_moeda_origem": id_origem,
            "id_moeda_destino": id_destino,
            "valor_origem": dados.valor_origem,
            "valor_destino": valor_destino,
            "taxa_percentual": self.TAXA_CONVERSAO,
            "taxa_valor": taxa_valor_origem,
            "cotacao_utilizada": cotacao,
        })
        
        return self.obter_saldos_por_endereco(endereco_carteira)

    def transferir(self, endereco_origem: str, dados: TransferenciaRequest):
        if not self._validar_chave_privada(endereco_origem, dados.chave_privada_origem):
            raise ValueError("Chave privada inválida para a carteira de origem.")

        if not self.repo.buscar_por_endereco(dados.endereco_destino):
            raise ValueError("Carteira de destino não encontrada.")

        id_moeda = self._buscar_id_moeda(dados.codigo_moeda)
        saldo_origem = self.repo.buscar_saldo(endereco_origem, id_moeda)
        
        taxa_valor = dados.valor * self.TAXA_TRANSFERENCIA
        valor_total_debito = dados.valor + taxa_valor
        valor_liquido_destino = dados.valor
        
        if saldo_origem < valor_total_debito:
            raise ValueError("Saldo insuficiente para transferência + taxa.")

        self.repo.atualizar_saldo(endereco_origem, id_moeda, -valor_total_debito)
        
        self.repo.atualizar_saldo(dados.endereco_destino, id_moeda, valor_liquido_destino)

        self.repo.registrar_transferencia_db({
            "endereco_origem": endereco_origem,
            "endereco_destino": dados.endereco_destino,
            "id_moeda": id_moeda,
            "valor": dados.valor,
            "taxa_valor": taxa_valor,
        })
        
        return self.obter_saldos_por_endereco(endereco_origem)