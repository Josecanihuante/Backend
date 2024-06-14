from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/basicauth",
                   tags= ["authentication"],
                   responses= {404:{"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    name: str
    surname: str
    profesion: str
    email: str
    disabled: bool


class UserDB(User):
    password: str

users_db =  {
    "JoseCanihuante":{
        "username": "JoseCanihuante",
        "name": "Jose",
        "surname": "Canihuante",
        "profesion": "Científico de Datos",
        "email": "jmcanihuante@hurtadohosp.cl",
        "disabled": False,
        "password": "Jesusteama12345"
    },
    "YubiPacheco":{
        "username": "YubiPacheco",
        "name": "Yubitsa",
        "surname": "Pacheco",
        "profesion": "Kinesiólogo",
        "email": "cragestiondecasos@hurtadohosp.cl",
        "disabled": True,
        "password": "12345"
    },
    "JavieraMacaya":{
        "username": "JaviMacaya",
        "name": "Javiera",
        "surname": "Macaya",
        "profesion": "Enfermera",
        "email": "jmacaya@hurtadohosp.cl",
        "disabled": False,
        "password": "6789"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user: 
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, 
            detail= "Credenciales de Autenticación inválidas", 
            headers = {"WWW-Autenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(
        status.HTTP_400_BAD_REQUEST, 
        detail= "Usuario inactivo")
    return user

@router.post("/login/")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
                            
    if form.password != user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

@router.get("/users/")
async def users():
    return users_db

    