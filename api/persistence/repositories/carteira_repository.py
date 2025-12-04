import os
import secrets
import hashlib
from typing import Dict, Any, Optional, List
from decimal import Decimal

from sqlalchemy import text
from api.persistence.db import get_connection


class CarteiraRepository:

    def buscar_id_moeda_por_codigo(self, codigo_moeda: str) -> Optional[int]:
        with get_connection() as conn:
            query = text("SELECT id_moeda FROM MOEDA WHERE codigo = :codigo")
            return conn.execute(query, {"codigo": codigo_moeda}).scalar_one_or_none()

    def buscar_saldo(self, endereco_carteira: str, id_moeda: int) -> Optional[Decimal]:
        with get_connection() as conn:
            query = text("SELECT saldo FROM SALDO_CARTEIRA WHERE endereco_carteira = :endereco AND id_moeda = :id_moeda")
            resultado = conn.execute(query, {"endereco": endereco_carteira, "id_moeda": id_moeda}).scalar_one_or_none()
            return resultado if resultado is not None else Decimal(0)

    def listar_saldos_por_endereco(self, endereco_carteira: str) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            query = text("""
                SELECT S.saldo, M.codigo
                FROM SALDO_CARTEIRA S
                JOIN MOEDA M ON S.id_moeda = M.id_moeda
                WHERE S.endereco_carteira = :endereco
            """)
            return conn.execute(query, {"endereco": endereco_carteira}).mappings().all()

    def buscar_hash_privada(self, endereco_carteira: str) -> Optional[str]:
        with get_connection() as conn:
            query = text("SELECT hash_chave_privada FROM CARTEIRA WHERE endereco_carteira = :endereco")
            return conn.execute(query, {"endereco": endereco_carteira}).scalar_one_or_none()

    def criar(self) -> Dict[str, Any]:
        private_key_size: int = int(os.getenv("PRIVATE_KEY_SIZE") or 32)
        public_key_size: int = int(os.getenv("PUBLIC_KEY_SIZE") or 16)
        
        chave_privada = secrets.token_hex(private_key_size) 
        endereco = secrets.token_hex(public_key_size) 
        
        hash_privada = hashlib.sha256(chave_privada.encode()).hexdigest()

        with get_connection() as conn:
            row = conn.execute(
                text("""
                    INSERT INTO carteira (endereco_carteira, hash_chave_privada)
                    VALUES (:endereco, :hash_privada)
                    RETURNING endereco_carteira, data_criacao, status, hash_chave_privada
                """),
                {"endereco": endereco, "hash_privada": hash_privada},
            ).mappings().first()
            
            id_moedas = conn.execute(text("SELECT id_moeda FROM MOEDA")).scalars().all()
            
            for id_moeda in id_moedas:
                 conn.execute(
                    text("""
                        INSERT INTO SALDO_CARTEIRA (endereco_carteira, id_moeda, saldo)
                        VALUES (:endereco, :id_moeda, 0)
                    """),
                    {"endereco": endereco, "id_moeda": id_moeda},
                )

        carteira = dict(row)
        carteira["chave_privada"] = chave_privada  
        return carteira

    def atualizar_saldo(self, endereco_carteira: str, id_moeda: int, valor_mudanca: Decimal):
        with get_connection() as conn:
            query = text("""
                UPDATE SALDO_CARTEIRA
                SET saldo = saldo + :valor_mudanca, data_atualizacao = CURRENT_TIMESTAMP
                WHERE endereco_carteira = :endereco AND id_moeda = :id_moeda
            """)
            conn.execute(query, {
                "valor_mudanca": valor_mudanca, 
                "endereco": endereco_carteira, 
                "id_moeda": id_moeda
            })

    def somar_saldo_global(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            query = text("""
                SELECT M.codigo AS codigo_moeda, SUM(S.saldo) AS saldo_total
                FROM SALDO_CARTEIRA S
                JOIN MOEDA M ON S.id_moeda = M.id_moeda
                GROUP BY M.codigo
                HAVING SUM(S.saldo) > 0;
            """)
            return conn.execute(query).mappings().all()

    def registrar_movimento_simples(self, endereco: str, id_moeda: int, tipo: str, valor: Decimal, taxa: Decimal):
        with get_connection() as conn:
            query = text("""
                INSERT INTO DEPOSITO_SAQUE 
                (endereco_carteira, id_moeda, tipo, valor, taxa_valor)
                VALUES (:endereco, :id_moeda, :tipo, :valor, :taxa)
            """)
            conn.execute(query, {
                "endereco": endereco, 
                "id_moeda": id_moeda, 
                "tipo": tipo, 
                "valor": valor, 
                "taxa": taxa
            })
            
    def registrar_conversao_db(self, dados: Dict[str, Any]):
        campos = ', '.join(dados.keys())
        valores = ', '.join(f':{k}' for k in dados.keys())
        query = text(f"INSERT INTO CONVERSAO ({campos}) VALUES ({valores})")
        with get_connection() as conn:
            conn.execute(query, dados)

    def registrar_transferencia_db(self, dados: Dict[str, Any]):
        campos = ', '.join(dados.keys())
        valores = ', '.join(f':{k}' for k in dados.keys())
        query = text(f"INSERT INTO TRANSFERENCIA ({campos}) VALUES ({valores})")
        with get_connection() as conn:
            conn.execute(query, dados)

    def buscar_por_endereco(self, endereco_carteira: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            query = text("SELECT endereco_carteira, data_criacao, status, hash_chave_privada FROM carteira WHERE endereco_carteira = :endereco")
            return conn.execute(query, {"endereco": endereco_carteira}).mappings().first()

    def listar(self) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            query = text("SELECT endereco_carteira, data_criacao, status, hash_chave_privada FROM carteira")
            return [dict(r) for r in conn.execute(query).mappings().all()]

    def atualizar_status(self, endereco_carteira: str, status: str) -> Optional[Dict[str, Any]]:
        with get_connection() as conn:
            conn.execute(
                text("UPDATE carteira SET status = :status WHERE endereco_carteira = :endereco"),
                {"status": status, "endereco": endereco_carteira},
            )
            query = text("SELECT endereco_carteira, data_criacao, status, hash_chave_privada FROM carteira WHERE endereco_carteira = :endereco")
            return conn.execute(query, {"endereco": endereco_carteira}).mappings().first()