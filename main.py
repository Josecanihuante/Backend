from fastapi import Body, FastAPI, status
from pydantic import BaseModel
from typing import Union
from enum import Enum
from fastapi.routing import APIRoute
from typing import Set, Union
from fastapi.responses import JSONResponse
from Routers import pacientes_db, users, patients, basic_auth_users, jwt_auth_users, usuarios_db
from fastapi.staticfiles import StaticFiles

#inicia el server: uvicorn main:app --reload

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()

class ModelName(str, Enum):
    alexnet = "alexnet"
    lenet = "lenet"
    resnet = "resnet"

app = FastAPI()

app.include_router(patients.router)
app.include_router(pacientes_db.router)
app.include_router(users.router)
app.include_router(usuarios_db.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.mount("/Statics", StaticFiles(directory="Statics"), name="Statics")


@app.get("/")
async def read_root():
    return {"Hola FastAPI"}

@app.get("/url")
async def read_url():
    return {"url_HPH": "www.hph.cl"}

@app.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_price": item.price, "item_id": item_id}

@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    return item

def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

