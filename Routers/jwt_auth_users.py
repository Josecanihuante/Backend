from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
SECRET = "c0a95fe2566d34c841713896a56a352b1ce27357e40be2b9fb095beaad552668"
ACCESS_TOKEN_DURATION = 1

router = APIRouter(prefix="/auth",
                   tags= ["authentication"],
                   responses= {404:{"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes= "bcrypt")

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
        "password": "$2a$12$VFKo9Gg.HBBI275f6sPhA.UaUfDN71/eWwxgsG2GNPomApImbRdGO"
    },
    "YubiPacheco":{
        "username": "YubiPacheco",
        "name": "Yubitsa",
        "surname": "Pacheco",
        "profesion": "Kinesiólogo",
        "email": "cragestiondecasos@hurtadohosp.cl",
        "disabled": False,
        "password": "$2a$12$xUn.iibHJhQGbE3DcXlpReGc/HbldaZB9pzjuWppu5/hNjW7g3uIq"
    },
    "JavieraMacaya":{
        "username": "JaviMacaya",
        "name": "Javiera",
        "surname": "Macaya",
        "profesion": "Enfermera",
        "email": "jmacaya@hurtadohosp.cl",
        "disabled": False,
        "password": "$2a$12$heZ0V15YWW/mnZK6jjPJQ.kQk1wqb38QpUnWh8wGz0CcRdfe0zn6q"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exeption = HTTPException(
                status.HTTP_401_UNAUTHORIZED, 
                detail= "Credenciales de Autenticación inválidas", 
                headers = {"WWW-Autenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exeption

    except JWTError: 
        raise exeption
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):   
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
                            
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_DURATION),  }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

@router.get("/users/")
async def users():
    return users_db