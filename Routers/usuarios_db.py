from fastapi import APIRouter, status
from DB.client import db_client
from DB.models.user import User
from DB.schemas.user import user_schema


router = APIRouter(prefix="/usersdb",
                   tags= ["usersdb"],
                   responses= {status.HTTP_404_NOT_FOUND:{"message": "No encontrado"}})

#inicia el server: uvicorn users:app --reload

users_list = []

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

@router.post("/", response_model= User, status_code=status.HTTP_201_CREATED)
async def post_user(user: User):
    #if type(search_user(user.id)) == User:
    #    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "El usuario ya existe")

    #else:
    user_dict = dict(user)
    del user_dict["id"]
    
    id =  db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id":id}))     
    return User(**new_user)

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
    
