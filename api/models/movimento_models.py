from pydantic import BaseModel
from decimal import Decimal

class DepositoRequest(BaseModel):
    codigo_moeda: str
    valor: Decimal

class SaqueRequest(BaseModel):
    codigo_moeda: str
    valor: Decimal
    chave_privada: str

class ConversaoRequest(BaseModel):
    chave_privada: str
    codigo_origem: str
    codigo_destino: str
    valor_origem: Decimal

class TransferenciaRequest(BaseModel):
    chave_privada_origem: str
    endereco_destino: str
    codigo_moeda: str
    valor: Decimal