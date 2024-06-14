from fastapi import APIRouter, status, HTTPException
from DB.client import db_client
from DB.models.actividades import Actividad
from DB.schemas.actividad import actividad_schema, actividades_schema
from bson import ObjectId

router = APIRouter(prefix="/actividadesdb",
                   tags= ["actividadesdb"],
                   responses= {status.HTTP_404_NOT_FOUND:{"message": "No encontrado"}})

#inicia el server: uvicorn users:app --reload

@router.get("/list/", response_model=list[Actividad])
async def actividades():
    return actividades_schema(db_client.actividades.find())

#Path
@router.get("/{id}")
async def actividad(id: str):
    return search_actividad("_id", ObjectId(id))

@router.post("/", response_model= Actividad, status_code=status.HTTP_201_CREATED)
async def post_actividad(actividad: Actividad):
    if type(search_actividad("cama", actividad.cama)) == Actividad:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "La actividad ya existe")

    else:
        actividad_dict = dict(actividad)
    del actividad_dict["id"]
    
    id =  db_client.actividades.insert_one(actividad_dict).inserted_id

    new_actividad = actividad_schema(db_client.actividades.find_one({"_id":id}))     
    return Actividad(**new_actividad)

@router.put("/")
async def put_actividad(actividad: Actividad):

    actividad_dict = dict(actividad)
    del actividad_dict["id"]
   
    try:
        db_client.actividades.find_one_and_replace({"_id":ObjectId(actividad.id)}, actividad_dict)
    except:    
        return  {"error":"No se ha actualizado la actividad"}
    else:
        return search_actividad("_id", ObjectId(actividad.id))

@router.delete("/{id}")
async def delete_actividad(id:str):
        
        found = db_client.actividades.find_one_and_delete({"_id":ObjectId(id)})
                  
        if not found:
            return  {"error":"No se ha eliminado la actividad"}
        
        return {"message": "la actividad fue eliminado"}

@router.patch("/{id}")
async def patch_actividad(id: str, actividad: Actividad):
    actividad_dict = dict(actividad)
    del actividad_dict["id"]

    try:
        updated_actividad = db_client.actividades.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": actividad_dict},
            return_document=True 
        )
    except Exception as e:
        return {"error": f"No se ha actualizado la actividad: {str(e)}"}
    else:
        if updated_actividad:
            return updated_actividad
        else:
            return {"message": "Actividad no encontrada"}



def search_actividad(field: str, key):
    try:
        actividad = db_client.actividades.find_one({field: key})
        return Actividad(**actividad_schema(actividad))
    except: 
        return  {"error":"No se ha encontrado la actividad"} 