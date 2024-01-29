import logging
import bcrypt

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from database.db import Session, get_db
from src.general.JWTFunctions import createJWTToken

from src.general.constant import USER, ADMIN
from src.general.response import error_response, get_message
from src.book_management_api.authentication.pydentic import auth_pydentic as pydanticSchemas
from src.book_management_api.authentication.CRUD import auth_CRUD as AuthCRUD

router = APIRouter()

@router.post("/login",response_model=pydanticSchemas.LoginResponse)
def login(db: Session = Depends(get_db), user: OAuth2PasswordRequestForm = Depends()):
    """
    Login a user. options are "admin", "user"
    """
    try:
            req_scopes = user.scopes
            
            if len(req_scopes) > 1:
                logging.info("More than one scope selected")
                return error_response(get_message("auth_login", "scope_greater"))
            if len(req_scopes) < 1:
                logging.info("No scope selected")
                return error_response(get_message("auth_login", "scope_lesser"))
        
            # validation of scope
            if req_scopes[0] not in (ADMIN, USER):
                logging.info("Invalid scope selected")
                return error_response(get_message("auth_login", "invalid_scope"))

            existing_user = AuthCRUD.getUserByEmailID(db, user.username)

            if not existing_user:
                logging.info("Invalid login credentials entered, Email ID not exist in database !!  ")
                return error_response(get_message("auth_login", "invalid_credential"), 401)

            #check the password is correct or not
            if not bcrypt.hashpw(
                    user.password.strip().encode("utf-8"), existing_user.password.encode("utf-8")
            ):
                logging.info("Invalid login credentials entered, Incorrect password !!")
                return error_response(get_message("auth_login", "invalid_credential"), 401)
        
            data = {
                "scopes": req_scopes,
                "ID": str(existing_user.id),
                "email": existing_user.username if req_scopes[0] == ADMIN or req_scopes[0] == USER else existing_user.id
            }
            
            jwt_token = createJWTToken(data)

            login_data = jsonable_encoder(existing_user)
            
            login_data['email'] = user.username if req_scopes[0] == ADMIN or req_scopes[0] == USER else existing_user.username

            return {
                "user": login_data,
                "access_token": jwt_token,
                "token_type": "bearer"
            }
    
    except ArithmeticError as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)
