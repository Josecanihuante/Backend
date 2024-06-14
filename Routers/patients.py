from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/pacientes",
                   tags= ["pacientes"],
                   responses= {404:{"message": "No encontrado"}})

class Paciente(BaseModel):
    id: int
    name: str
    surname: str
    diagnostico: str
    comorbilidad: str
    cama: int
    servicio: str

pacientes_list = [Paciente(id = 1, name = "Godolfredo", surname = "Pinto", diagnostico = "Infección Cateter", comorbilidad = "Insuficiencia Renal, Artrosis de Rodilla, DM2, HTA", cama = 609, servicio = "MQ6"), 
                  Paciente(id = 2, name = "Rosa", surname = "Martínez", diagnostico = "Prótesis Total de Rodilla", comorbilidad = "DM2", cama = 608, servicio = "MQ6")]

@router.get("/list/")
async def pacientes():
    return pacientes_list

@router.get("/{id}")
async def pacientepath(id: int):
    return search_paciente(id)
    
#Query
@router.get("/")
async def pacientequery(id: int):
    return search_paciente(id)

@router.post("/", response_model= Paciente, status_code=201)
async def post_paciente(paciente: Paciente):
    if type(search_paciente(paciente.id)) == Paciente:
        raise HTTPException(status_code= 204, detail= "El usuario ya existe")
        return {"error": "El usuario ya existe"}
    else:
        pacientes_list.append(paciente)
        return paciente

@router.put("/")
async def put_paciente(paciente: Paciente):

    found = False

    for index, saved_paciente in enumerate(pacientes_list):
        if saved_paciente.id == paciente.id:
            pacientes_list[index] = paciente
        found = True
    
    if not found:
        return  {"error":"No se ha actualizado el usuario"}
    else:
        return paciente

@router.delete("/{id}")
async def delete_paciente(id: int):
        
        found = False

        for index, saved_paciente in enumerate(pacientes_list):
            if saved_paciente.id == id:
                del pacientes_list[index]
                found = True   
        
        if not found:
            return  {"error":"No se ha eliminado el usuario"}
        
@router.patch("/{id}/")
async def update_paciente(id: int, update_data: dict):
    for paciente in pacientes_list:
        if paciente.id == id:
            for key, value in update_data.items():
                setattr(paciente, key, value)
            return {"message": "Usuario actualizado correctamente"}
    
    return {"error": "No se ha encontrado el usuario"}

def search_paciente(id: int):
    pacientes = filter(lambda paciente: paciente.id == id, pacientes_list)
    try:
        return list(pacientes)[0]
    except: 
        return  {"error":"No se ha encontrado el usuario"}