from typing import Union
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/usuarios",
                   tags= ["usuarios"],
                   responses= {404:{"message": "No encontrado"}})

#inicia el server: uvicorn users:app --reload

class User(BaseModel):
    id: int
    name: str
    surname: str
    profesion: str
    servicio: str

users_list = [User(id = 1, name = "Jose", surname = "Canihuante", profesion = "Científico de Datos", servicio ="CR Adulto"),
              User(id = 2, name = "Yubitsa", surname = "Pacheco", profesion = "Kinesiólogo", servicio = "CR Adulto"),
              User(id = 3, name = "Javiera", surname = "Macaya", profesion = "Enfermera", servicio = "CR Adulto")]

@router.get("/list/")
async def users():
    return users_list

#Path
@router.get("/{id}")
async def userpath(id: int):
    return search_user(id)
    
#Query
@router.get("/")
async def userquery(id: int):
    return search_user(id)

@router.post("/", response_model= User, status_code=201)
async def post_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code= 204, detail= "El usuario ya existe")

    else:
        users_list.append(user)
        return user

@router.put("/")
async def put_user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
        found = True
    
    if not found:
        return  {"error":"No se ha actualizado el usuario"}
    else:
        return user

@router.delete("/{id}")
async def delete_user(id: int):
        
        found = False

        for index, saved_user in enumerate(users_list):
            if saved_user.id == id:
                del users_list[index]
                found = True
                
        if not found:
            return  {"error":"No se ha eliminado el usuario"}

@router.patch("/{id}/")
async def update_user(id: int, update_data: dict):
    for user in users_list:
        if user.id == id:
            for key, value in update_data.items():
                setattr(user, key, value)
            return {"message": "Usuario actualizado correctamente"}
    
    return {"error": "No se ha encontrado el usuario"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except: 
        return  {"error":"No se ha encontrado el usuario"}
    
