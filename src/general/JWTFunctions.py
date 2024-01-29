from jose import JWTError, jwt
from typing import Optional
from datetime import timedelta, datetime

from config.config import setting

def createJWTToken(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.JWTSECRETKEY, setting.JWTALGORITHM)

    return encoded_jwt


def decodeToken(token: str):
    try:
        payload = jwt.decode(token, setting.JWTSECRETKEY)
        return payload
    except JWTError:
        print("error is decode token")
        raise JWTError
