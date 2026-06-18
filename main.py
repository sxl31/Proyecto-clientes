from fastapi import FastAPI, HTTPException
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar

app = FastAPI()

lista_clientes:list[Cliente] = []


# endpoint para listar todos los clientes
@app.get("/clientes", response_model=list[Cliente])
async def listar_clientes():
    return lista_clientes

# endpoint para listar un solo cliente
@app.get("/clientes/{cliente_id}", response_model=Cliente)
async def listar_clientes(cliente_id: int):
    #recorrer la lista clientes
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == cliente_id:
            return obj_cliente



# endpoint para crear un solo cliente y agregar a lista
@app.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear):
   cliente_val = Cliente.model_validate(datos_cliente.model_dump())
   #generar el id  
   id_cliente = len(lista_clientes) + 1
   cliente_val.id = id_cliente
   lista_clientes.append(cliente_val)
   return cliente_val
#editar un cliente y agregar a la lsista
@app.patch("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(cliente_id: int, datos_cliente: ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == cliente_id:
            cliente_val = Cliente.model_validate(
                datos_cliente.model_dump()
            )
            cliente_val.id = cliente_id
            lista_clientes[i] = cliente_val
            return cliente_val
    raise HTTPException(
        status_code=400,
        detail=f"El cliente con id {cliente_id}, no existe"
    )

#endpoint eliminar
@app.delete("/clientes/{cliente_id}")
async def eliminar_cliente(cliente_id: int):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == cliente_id:
            del lista_clientes[i]

            return {
                "mensaje": f"Cliente con id {cliente_id} eliminado correctamente"
            }

    raise HTTPException(
        status_code=404,
        detail=f"El cliente con id {cliente_id} no existe"
    )