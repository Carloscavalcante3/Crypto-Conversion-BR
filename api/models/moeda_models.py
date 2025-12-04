from pydantic import BaseModel
from typing import Literal
from decimal import Decimal

class Moeda(BaseModel):
    id_moeda: int
    codigo: str
    nome: str
    tipo: Literal['CRYPTO', 'FIAT']

class Saldo(BaseModel):
    codigo_moeda: str
    saldo: Decimal