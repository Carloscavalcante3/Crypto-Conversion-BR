from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.services.carteira_service import CarteiraService
from api.persistence.repositories.carteira_repository import CarteiraRepository
from api.models.carteira_models import Carteira, CarteiraCriada
from api.models.moeda_models import Saldo
from api.models.movimento_models import DepositoRequest, SaqueRequest, ConversaoRequest, TransferenciaRequest


router = APIRouter(prefix="/carteiras", tags=["Carteiras e Movimentações"])


def get_carteira_service() -> CarteiraService:
    repo = CarteiraRepository()
    return CarteiraService(repo)


@router.post("", response_model=CarteiraCriada, status_code=201)
def criar_carteira(service: CarteiraService = Depends(get_carteira_service),)->CarteiraCriada:
    try:
        return service.criar_carteira()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao criar carteira: " + str(e))

@router.get("", response_model=List[Carteira])
def listar_carteiras(service: CarteiraService = Depends(get_carteira_service)):
    return service.listar()

@router.get("/{endereco_carteira}", response_model=Carteira)
def buscar_carteira(endereco_carteira: str, service: CarteiraService = Depends(get_carteira_service),):
    try:
        return service.buscar_por_endereco(endereco_carteira)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{endereco_carteira}/saldos", response_model=List[Saldo])
def consultar_saldos(endereco_carteira: str, service: CarteiraService = Depends(get_carteira_service)):
    try:
        return service.obter_saldos_por_endereco(endereco_carteira)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/saldos/global", response_model=List[Saldo], summary="Consulta o saldo total da aplicação por moeda")
def consultar_saldos_globais(service: CarteiraService = Depends(get_carteira_service)):
    return service.obter_saldo_global()

@router.delete("/{endereco_carteira}", response_model=Carteira)
def bloquear_carteira(endereco_carteira: str, service: CarteiraService = Depends(get_carteira_service),):
    try:
        return service.bloquear(endereco_carteira)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{endereco_carteira}/depositos")
def fazer_deposito(endereco_carteira: str, dados: DepositoRequest, service: CarteiraService = Depends(get_carteira_service)):
    try:
        return service.depositar(endereco_carteira, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{endereco_carteira}/saques")
def fazer_saque(endereco_carteira: str, dados: SaqueRequest, service: CarteiraService = Depends(get_carteira_service)):
    try:
        return service.sacar(endereco_carteira, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{endereco_carteira}/conversoes")
async def fazer_conversao(endereco_carteira: str, dados: ConversaoRequest, service: CarteiraService = Depends(get_carteira_service)):
    try:
        return await service.converter_moeda(endereco_carteira, dados)
    except (ValueError, httpx.HTTPStatusError) as e:
        detail = str(e) if isinstance(e, ValueError) else "Erro ao obter cotação da Coinbase."
        raise HTTPException(status_code=400, detail=detail)

@router.post("/{endereco_origem}/transferencias")
def fazer_transferencia(endereco_origem: str, dados: TransferenciaRequest, service: CarteiraService = Depends(get_carteira_service)):
    try:
        return service.transferir(endereco_origem, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))