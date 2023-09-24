from http.client import HTTPException
from typing import Annotated
from fastapi import Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from cryptography.fernet import Fernet
from starlette import status

import base64

from config.database import connect_db

SECRET_KEY = "mendavenkatasuresh"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


secret_key = b'mendavenkatasuresh'
while len(secret_key) < 32:
    secret_key += secret_key

secret_key = secret_key[:32]
cipher_suite = Fernet(base64.urlsafe_b64encode(secret_key))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# fake_users_db = [
#     {
#         "id": 1,
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "gAAAAABk_IxcnuQUPedERvL1EcVpuyyzA7PycRx4CX3WJlchiZRLLAXQjlBHHpYl4b2_SIH6hD7wlaBcdnUcSFZQS7WREFoU2Q==",  # johndoe
#         "disabled": False,
#     },
#     {
#             "id": 2,
#             "username": "suresh",
#             "full_name": "venkat suresh",
#             "email": "suresh@example.com",
#             "hashed_password": "gAAAAABk_Iw8WGlYGen1U5sflD2AiiJ0VMTdFNcIm2GroOrLK9a7F-0fHqlI0KYQhrBQ43Tf4-VWyJbC1PmY-9cK2RDYjUUdDg==",  # suresh
#             "disabled": False,
#     },
#     {
#             "id": 3,
#             "username": "saikrishna",
#             "full_name": "saikrishna",
#             "email": "saikrishna@example.com",
#             "hashed_password": "gAAAAABk_IpRdy4jFJtBloSCmvnj5UgWqx9ujTg_JR6AO5_JZtqmrxYCnOA0nS0yoXXc64Pjp3zTN7Q38GiFBKouA8Vrx1lPtw==",  # suresh
#             "disabled": False,
#     }
# ]

# GET USER DATA FROM DATABASE
fake_users_db = []

def getall_users():
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = "select * from users"
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(e)
        return []

if not fake_users_db:
    fake_users_db = getall_users()

class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: dict


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    return (plain_password == cipher_suite.decrypt(hashed_password).decode())


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    for user_dict in db:
        if user_dict["username"] == username or user_dict["email"] == username:
            return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Session expired.", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

