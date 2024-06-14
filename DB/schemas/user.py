
def user_schema(user) -> dict: 
    return {"id": str(user["_id"]),
            "name": user["name"],   
            "surname": user["surname"],
            "profesion": user["profesion"],
            "servicio": user["servicio"]}