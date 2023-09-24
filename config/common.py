from http.client import HTTPException
from starlette import status
from config.authentication import oauth2_scheme, SECRET_KEY, ALGORITHM
from fastapi import Depends
from jose import jwt

import re

# ----------------------------------------- AUTH & TOKEN VERIFICATION --------------------------------------------------
def is_authorize(token):
    resp = auth_verification(token)
    if resp is not True:
        raise HTTPException(status_code=401, detail=resp)
    else:
        return resp

def auth_verification(token):
    if (user_authentication()):
        if (verifytoken(token) == True):
            return True
        else:
            return {"status": 401, "data": "Token has expired."}
    else:
        return {"status": 403, "data": "Authorized User."}


# ----------------------------------------- AUTHORIZATION --------------------------------------------------------------
def user_authentication(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized. Please provide a valid token.",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    return True


# ----------------------------------------- TOKEN VERIFICATION ---------------------------------------------------------
def verifytoken(token: str):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration_time = token_data["exp"]
        return True # {"status": 200, "data": f"Token expiration time: {expiration_time}"}
    except jwt.ExpiredSignatureError:
        return {"status": 400, "data": "Token has expired."}
    except jwt.JWTError:
        return {"status": 404, "data": "Token decoding failed."}


# ----------------------------------------- EMAIL VERIFICATION ---------------------------------------------------------
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
