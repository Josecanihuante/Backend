def actividad_schema(actividad) -> dict: 
    return {"id": str(actividad["_id"]), 
            "paciente": actividad["paciente"],
            "asunto": actividad["asunto"],
            "descripcion": actividad["descripcion"],
            "estado": actividad["estado"],
            "asignado_a": actividad["asignado_a"],
            "cama": actividad["cama"],
            "fecha_inicio": actividad["fecha_inicio"],
            "fecha_termino": actividad["fecha_termino"],
            }

def actividades_schema(actividades) -> list:
    return [actividad_schema(actividad) for actividad in actividades]