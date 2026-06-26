from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine

# IMPORTAR TODOS LOS MODELOS
from .modelos.clientes import Cliente
from .modelos.facturas import Factura
from .modelos.transacciones import Transaccion

nombre_bd = "bd_clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

# Motor de la base de datos
motor_bd = create_engine(url_bd)

# Crear las tablas
def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield

# Obtener sesión
def obtener_sesion():
    with Session(motor_bd) as mi_sesion:
        yield mi_sesion

# Dependencia
Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]