from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ..conexion_bd import Sesion_dependencia
from ..modelos.clientes import Cliente
from ..modelos.facturas import Factura, FacturaCrear, FacturaEditar, FacturaLeer, FacturaLeerCompuesta

rutas_facturas = APIRouter()


@rutas_facturas.get("/facturas", response_model=list[FacturaLeerCompuesta])
async def listar_facturas(sesion: Sesion_dependencia):
    consulta = select(Factura)
    lista_facturas = sesion.exec(consulta).all()
    return lista_facturas


@rutas_facturas.get("/facturas/{factura_id}", response_model=FacturaLeer)
async def listar_factura(factura_id: int, sesion: Sesion_dependencia):
    factura_bd = sesion.get(Factura, factura_id)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe."
        )

    return factura_bd


@rutas_facturas.post("/facturas/{cliente_id}", response_model=FacturaLeer)
async def crear_factura(
    cliente_id: int,
    datos_factura: FacturaCrear,
    mi_sesion: Sesion_dependencia
):
    cliente_bd = mi_sesion.get(Cliente, cliente_id)

    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El cliente con id {cliente_id}, no existe."
        )

    # Agregar el cliente_id ANTES de validar
    datos = datos_factura.model_dump()
    datos["cliente_id"] = cliente_id

    factura_val = Factura.model_validate(datos)

    factura_val.cliente = cliente_bd

    mi_sesion.add(factura_val)
    mi_sesion.commit()
    mi_sesion.refresh(factura_val)

    return factura_val


@rutas_facturas.patch("/facturas/{id_factura}", response_model=FacturaLeer)
async def editar_factura(
    id_factura: int,
    datos_factura: FacturaEditar,
    mi_sesion: Sesion_dependencia
):
    factura_bd = mi_sesion.get(Factura, id_factura)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {id_factura}, no existe."
        )

    factura_dict = datos_factura.model_dump(exclude_unset=True)
    factura_bd.sqlmodel_update(factura_dict)

    mi_sesion.add(factura_bd)
    mi_sesion.commit()
    mi_sesion.refresh(factura_bd)

    return factura_bd


@rutas_facturas.delete("/facturas/{id_factura}", response_model=FacturaLeer)
async def eliminar_factura(
    id_factura: int,
    mi_sesion: Sesion_dependencia
):
    factura_bd = mi_sesion.get(Factura, id_factura)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {id_factura}, no existe."
        )

    mi_sesion.delete(factura_bd)
    mi_sesion.commit()

    return factura_bd