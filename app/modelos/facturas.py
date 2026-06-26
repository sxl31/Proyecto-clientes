from sqlmodel import SQLModel, Field
from pydantic import computed_field
from datetime import datetime

from .transacciones import Transaccion
from .clientes import Cliente


class FacturaBase(SQLModel):
    fecha: str = str(datetime.now())
    cliente_id: int

    @computed_field
    @property
    def vr_total(self) -> float:
        return 0.0


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)