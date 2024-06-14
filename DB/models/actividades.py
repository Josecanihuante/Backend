from pydantic import BaseModel

class Actividad(BaseModel):
    id: str | None
    paciente: str
    asunto: str
    descripcion: str
    estado: str
    asignado_a: str
    cama: str | None
    fecha_inicio: str
    fecha_termino: str