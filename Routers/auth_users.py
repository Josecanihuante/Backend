from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    name: str
    surname: str
    profession: str
    email: str
    disabled: bool

class UserInDB(User):
    hashed_password: str


users_db = {
    "JoseCanihuante": {
        "username": "JoseCanihuante",
        "name": "Jose",
        "surname": "Canihuante",
        "profession": "Científico de Datos",
        "email": "jmcanihuante@hurtadohosp.cl",
        "disabled": False,
        "hashed_password": "$2b$12$5s2Ojy8j3Zqmd03M8H58buwXkjghlCil0tGZVKJ/n/ST1hp7IucOu"
    },
    "YubiPacheco":{
        "username": "YubiPacheco",
        "name": "Yubitsa",
        "surname": "Pacheco",
        "profesion": "Kinesiólogo",
        "email": "cragestiondecasos@hurtadohosp.cl",
        "disabled": False,
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

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@app.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Return the access token here
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(oauth2_scheme)):
    return current_user

@app.get("/users/")
async def users():
    return users_db