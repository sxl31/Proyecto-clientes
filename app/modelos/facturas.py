from datetime import datetime
from pydantic import computed_field
from sqlmodel import SQLModel, Field, Relationship

from .clientes import Cliente, ClienteLeer
from .transacciones import TransaccionLeer

class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now())


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    cliente_id: int = Field(foreign_key="cliente.id")

    cliente: Cliente = Relationship(back_populates="factura")

    transacciones: list["Transaccion"] = Relationship(back_populates="factura")


class FacturaLeer(FacturaBase):
    id: int
    cliente: ClienteLeer


class FacturaLeerCompuesta(FacturaLeer):
    transacciones: list[TransaccionLeer] = Field(default_factory=list)

    @computed_field
    @property
    def vr_total(self) -> float:
        return sum(
            t.cantidad * t.vr_unitario
            for t in self.transacciones
        )