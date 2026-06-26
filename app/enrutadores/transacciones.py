from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ..modelos.transacciones import (
    Transaccion,
    TransaccionCrear,
    TransaccionEditar
)
from ..modelos.facturas import Factura
from ..conexion_bd import Sesion_dependencia

rutas_transacciones = APIRouter()


# Listar todas las transacciones
@rutas_transacciones.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones(mi_sesion: Sesion_dependencia):
    lista_transacciones = mi_sesion.exec(select(Transaccion)).all()
    return lista_transacciones


# Listar una transacción
@rutas_transacciones.get("/transacciones/{id_transaccion}", response_model=Transaccion)
async def listar_transaccion(
    id_transaccion: int,
    mi_sesion: Sesion_dependencia
):
    transaccion_bd = mi_sesion.get(Transaccion, id_transaccion)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La transacción con id {id_transaccion} no existe."
        )

    return transaccion_bd


# Crear transacción
@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionCrear,
    mi_sesion: Sesion_dependencia
):
    factura_bd = mi_sesion.get(Factura, factura_id)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id} no existe."
        )

    transaccion_val = Transaccion.model_validate(
        datos_transaccion.model_dump()
    )

    transaccion_val.factura_id = factura_id

    mi_sesion.add(transaccion_val)
    mi_sesion.commit()
    mi_sesion.refresh(transaccion_val)

    return transaccion_val


# Editar transacción
@rutas_transacciones.patch(
    "/transacciones/{id_transaccion}",
    response_model=Transaccion
)
async def editar_transaccion(
    id_transaccion: int,
    datos_transaccion: TransaccionEditar,
    mi_sesion: Sesion_dependencia
):
    transaccion_bd = mi_sesion.get(Transaccion, id_transaccion)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La transacción con id {id_transaccion} no existe."
        )

    transaccion_dict = datos_transaccion.model_dump(exclude_unset=True)
    transaccion_bd.sqlmodel_update(transaccion_dict)

    mi_sesion.add(transaccion_bd)
    mi_sesion.commit()
    mi_sesion.refresh(transaccion_bd)

    return transaccion_bd


# Eliminar transacción
@rutas_transacciones.delete(
    "/transacciones/{id_transaccion}",
    response_model=Transaccion
)
async def eliminar_transaccion(
    id_transaccion: int,
    mi_sesion: Sesion_dependencia
):
    transaccion_bd = mi_sesion.get(Transaccion, id_transaccion)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La transacción con id {id_transaccion} no existe."
        )

    mi_sesion.delete(transaccion_bd)
    mi_sesion.commit()

    return transaccion_bd