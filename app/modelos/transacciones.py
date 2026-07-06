from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .facturas import Factura


class TransaccionBase(SQLModel):
    cantidad: int = Field(default=0)
    vr_unitario: float = Field(default=0.0)


class TransaccionCrear(TransaccionBase):
    pass


class TransaccionEditar(TransaccionBase):
    pass


class Transaccion(TransaccionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    factura_id: int | None = Field(default=None, foreign_key="factura.id")
    factura: "Factura" = Relationship(back_populates="transacciones")


class TransaccionLeer(TransaccionBase):
    id: int
    factura_id: int