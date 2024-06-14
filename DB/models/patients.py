from pydantic import BaseModel

class Patient(BaseModel):
    id: str | None
    name: str
    estado: str
    asignado_a: str
    comuna: str
    origen: str
    servicio: str
    cama: str
    diagnostico: str
    ingreso: str
    egreso: str
    tipo_egreso: str
