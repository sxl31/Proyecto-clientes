from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ..modelos.facturas import Factura, FacturaCrear, FacturaEditar
from ..modelos.clientes import Cliente
from ..conexion_bd import Sesion_dependencia

rutas_facturas = APIRouter()


# Listar todas las facturas
@rutas_facturas.get("/facturas", response_model=list[Factura])
async def listar_facturas(mi_sesion: Sesion_dependencia):
    lista_facturas = mi_sesion.exec(select(Factura)).all()
    return lista_facturas


# Listar una factura
@rutas_facturas.get("/facturas/{factura_id}", response_model=Factura)
async def listar_factura(factura_id: int, mi_sesion: Sesion_dependencia):
    factura_bd = mi_sesion.get(Factura, factura_id)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con id {factura_id}, no existe."
        )

    return factura_bd


# Crear factura
@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura)
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

    factura_val = Factura.model_validate(datos_factura.model_dump())

    # Guardar el id del cliente
    factura_val.cliente_id = cliente_id

    mi_sesion.add(factura_val)
    mi_sesion.commit()
    mi_sesion.refresh(factura_val)

    return factura_val


# Editar factura
@rutas_facturas.patch("/facturas/{id_factura}", response_model=Factura)
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


# Eliminar factura
@rutas_facturas.delete("/facturas/{id_factura}", response_model=Factura)
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