from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError

from .JWTFunctions import decodeToken

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes={
        "admin": "For admin",
        "user": "For user"
    }
)

def verifyToken(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    raw_token = token
    try:
        # Remove the Bearer from the token before verifying its validaty
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        payload = decodeToken(token)
        payload["token"] = raw_token
        user: str = payload.get("email")
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    tokenScopes = payload.get("scopes")
    if len(security_scopes.scopes) > 1:
        if tokenScopes[0] not in security_scopes.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Incorrect scopes, need the following scope: "
                       + security_scopes.scope_str,
                headers={"WWW-Authenticate": authenticate_value},
            )
    else:
        for scope in security_scopes.scopes:
            if scope not in tokenScopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Incorrect scopes, need the following scope: "
                           + security_scopes.scope_str,
                    headers={"WWW-Authenticate": authenticate_value},
                )

    return payload

