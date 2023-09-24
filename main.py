import socket
import uvicorn

from jose import jwt
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from config.authentication import Token, cipher_suite, oauth2_scheme, SECRET_KEY,ALGORITHM
from controller import UserController, ProductController

app = FastAPI()

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_authorize(token: str):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration_time = token_data["exp"]
        return True # {"status": 200, "data": f"Token expiration time: {expiration_time}"}
    except jwt.ExpiredSignatureError:
        return {"status": 400, "data": "Token has expired."}
    except jwt.JWTError:
        return {"status": 404, "data": "Token decoding failed."}



# ------------------------------------------   IPAddress   -------------------------------------------------------------
@app.get("/getipaddress", tags=["IP Address"])
async def get_system_ip():
    hostname = socket.gethostname()  # System Name
    ip_address = socket.gethostbyname(hostname)
    return {"ipaddress": ip_address}

# ------------------------------------------   DATE & TIME   -----------------------------------------------------------
@app.get("/getdatetime", tags=["Date & Time"])
async def get_system_datetime():
    current_timestamp = datetime.now()
    return current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

#--------------------------------------------- ENCODE & DECODE ---------------------------------------------------------
@app.get("/encode", tags=["ENCODE & DECODE"])
async def encode(password:str):
    return cipher_suite.encrypt(password.encode())

@app.get("/decode", tags=["ENCODE & DECODE"])
async def decode(password:str):
    return cipher_suite.decrypt(password).decode()

#--------------------------------------------- USERS -------------------------------------------------------------------
@app.get("/getallusers", tags=["USERS"])
async def getallusers():
    return UserController.getalluser()

@app.post("/register", tags=["USERS"])
async def create_user(username:str,full_name:str,email:str,password:str):
    return UserController.createuser(username,full_name,email,password)

@app.post("/token", response_model=Token, tags=["USERS"])
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return UserController.is_login(form_data)

@app.get("/getuserbyid", tags=["USERS"])
async def getuserbyid(id:int,token: str = Depends(oauth2_scheme)):
    is_authorize(token)
    return UserController.getuserbyid(id)

@app.post("/updateuser", tags=["USERS"])
async def update_user(id:int,data: str,token: str = Depends(oauth2_scheme)):
    is_authorize(token)
    return UserController.update_user(id,data)

@app.post("/deleteuser", tags=["USERS"])
async def delete_user(id:int,token: str = Depends(oauth2_scheme)):
    is_authorize(token)
    return UserController.delete_user(id)

#--------------------------------------------- PRODUCTS ----------------------------------------------------------------
@app.get("/getallproducts", tags=["PRODUCTS"])
async def getallproducts(token: str = Depends(oauth2_scheme)):
    resp = is_authorize(token)
    if(resp == True):
        return ProductController.getallproducts()
    else:
        return resp

@app.post("/createproduct", tags=["PRODUCTS"])
async def createproduct(name:str, token: str = Depends(oauth2_scheme)):
    is_authorize(token)
    return ProductController.create_product(name)

@app.post("/updateproduct", tags=["PRODUCTS"])
async def updateproduct(id:int,name:str,token: str = Depends(oauth2_scheme)):
    is_authorize(token)
    return ProductController.update_product(id,name)

@app.post("/deleteproduct", tags=["PRODUCTS"])
async def delete_product(id:int,token: str = Depends(oauth2_scheme)):
    is_authorize(token)
    return  ProductController.delete_product(id)
#--------------------------------------------- MAIN METHOD -------------------------------------------------------------
if __name__ == '__main__':
    # uvicorn.run(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)