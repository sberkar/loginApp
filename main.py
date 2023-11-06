from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session
import bcrypt
from jose import ExpiredSignatureError, jwt, JWTError
from datetime import timedelta, datetime

import random

import models, schema, database

models.database.Base.metadata.create_all(bind=database.engine)
BASE_PATH = Path(__file__).resolve().parent

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory=str(Path(BASE_PATH, "templates")))

@app.get('/jwt/user')
def getAccountByJWT(request: Request, db: Session = Depends(get_db)):
    auth_token = request.headers.get("Authorization").split(" ")[1]

    try:
        user = jwt.decode(auth_token, key=SECRET_KEY)
        user_obj = db.query(models.User).filter(models.User.email == user.get('email')).first()

        if not user_obj:
            return { 'msg': 'something went wrong'}
        return { 'name': user_obj.name, 'uid': user_obj.id, 'email': user_obj.email } 
    except ExpiredSignatureError as error:
        return False
    except JWTError as error:
        return False

app.mount('/static', StaticFiles(directory='static'), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.jinja", context={ "request": request })

@app.post("/jwt/logout")
def logout(request: Request, db: Session = Depends(get_db)):
    auth_token = request.headers.get('Authorization').split(' ')[1]

    try:
        decode_data = jwt.decode(auth_token, key=SECRET_KEY)
        user = db.query(models.User).filter(models.User.accessToken == auth_token)

        if not user.first():
            raise HTTPException(400, detail={ 'msg': { 'operation was unsuccessfull' }}) 
        user.update({ 'accessToken': ""})
        return True
    except ExpiredSignatureError as error:
        return False
    except JWTError as error:
        return False


@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html.jinja", context={ 'request': request})

@app.get("/creds")
def creds(request: Request):
    id = random.randint(0, 100)
    passwd = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()') for i in range(10))
    return templates.TemplateResponse("creds.jinja", context={'request': request, 'uid': id, 'passwd': passwd })

@app.get("/account")
def account(request: Request):
    return templates.TemplateResponse('account.jinja', context={ 'request': request })

@app.post("/register")
def postRegister(user: schema.CreateUser, db:  Session = Depends(get_db)):
    #checking email exists or not
    isUser = db.query(models.User).filter(models.User.email == user.email).first()
    if isUser != None:
        return { 'msg': "User Already Exists",
                'status': 400 
                }
    hashed_pass = bcrypt.hashpw(user.passwd.encode(), bcrypt.gensalt(12))
    user_obj = models.User(name = user.name, email = user.email, passwd = hashed_pass)
    db.add(user_obj)
    db.commit()
    return { 'msg': 'User Created Successfully',
            'status': 201
            }

@app.get('/login')
def login(request: Request):
    return templates.TemplateResponse("login.html.jinja", context={ 'request': request })

@app.post("/login")
def postLogin(user: schema.LoginUser, db: Session = Depends(get_db)):
    isUser = db.query(models.User).filter(models.User.email == user.email)
    if not isUser.first():
        raise HTTPException(status_code=404, detail={ 'msg': "please enter valid Credentials"})

    encoded_passwd = user.passwd.encode()
    passwd_from_db = isUser.first().passwd.encode()
    isPassValid = bcrypt.checkpw(encoded_passwd, passwd_from_db) 
    if not isPassValid:
        raise HTTPException(status_code=404, detail={ 'msg': "please enter valid credentials"})
    isUserCopy = { "name": isUser.first().name, "email": isUser.first().email, "exp": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS) }
    encoded_jwt = jwt.encode(isUserCopy, SECRET_KEY, algorithm=ALGORITHM)
    isUser.update({ "accessToken" : encoded_jwt})
    db.commit()
    return { "access_token": encoded_jwt}


@app.get("/jwt/verify")
async def jwtverify(request: Request, db: Session = Depends(get_db)):
    auth_token = request.headers.get("Authorization").split(" ")[1]

    try:
        user = jwt.decode(auth_token, key=SECRET_KEY)
        user_obj = db.query(models.User).filter(models.User.email == user.get('email')).first()
        if user_obj.accessToken == auth_token:
            return True
        return False
    except ExpiredSignatureError as error:
        return False
    except JWTError as error:
        return False


@app.get("/*")
def notfound():
    return { 404: "not found" }