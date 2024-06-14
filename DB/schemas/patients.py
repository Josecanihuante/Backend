def patient_schema(patient) -> dict: 
    return {"id": str(patient["_id"]),
            "name": patient["name"],   
            "estado": patient["estado"],
            "asignado_a": patient["asignado_a"],
            "comuna": patient["comuna"],
            "origen": patient["origen"],
            "servicio": patient["servicio"],
            "cama": patient["cama"],
            "diagnostico": patient["diagnostico"],
            "ingreso": patient["ingreso"],
            "egreso": patient["egreso"],
            "tipo_egreso": patient["egreso"]
            }

def patients_schema(patients) -> list:
    return [patient_schema(patient) for patient in patients]