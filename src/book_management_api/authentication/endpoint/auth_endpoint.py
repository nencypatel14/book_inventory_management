import logging
import os
import bcrypt
from jose import jwt
import requests

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.db import Session, get_db
from src.general.JWTFunctions import createJWTToken

from src.general.constant import USER, ADMIN
from src.general.response import error_response, get_message
from src.book_management_api.authentication.pydentic import auth_pydentic as pydanticSchemas
from src.book_management_api.authentication.CRUD import auth_CRUD as AuthCRUD
from config.config import setting

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


# @router.post("/google/signin")
# async def social_login(input_data: pydanticSchemas.GoogleSocialLoginRequest, db: Session = Depends(get_db)):
#     try:
#         headers = {
#                 "Content-Type":"application/x-www-form-urlencoded"
#             }
#         # Authorize the request with google
#         response = requests.post(
#             "https://accounts.google.com/o/oauth2/v2/auth", params={
#                 "code": input_data.code,       
#                 "client_id": os.environ.get(setting.GOOGLE_CLIENT_ID),
#                 "client_secret": os.environ.get(setting.GOOGLE_CLIENT_SECRET),
#                 "redirect_uri": os.environ.get(setting.GOOGLE_REDIRECT_URI),
#                 "grant_type": os.environ.get(setting.GOOGLE_GRANT_TYPE),
#             },headers=headers
#         )
#         token_data = response.json()
#         # Get user info with the token
#         user_info = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={
#             "Authorization": f"Bearer {token_data['access_token']}"
#         })
#         user_info_data = user_info.json()
#         email = user_info_data['email']
#         dbUser = AuthCRUD.getUserByEmailID(db, email)
#         if not dbUser:
#             logging.info("No user exists in the database with this email")
#             return error_response(get_message("auth_login", "no_social_account"), 401)
#         data = {
#             "ID": dbUser.ID,
#             "email":dbUser.email 
#         }
#         jwt_token = createJWTToken(data)
#         login_data = jsonable_encoder(dbUser._mapping)
#         login_data["password_updated"] = True
#         return {
#                 "user": login_data,
#                 "access_token": jwt_token,
#                 "token_type": "bearer",
#                 "social_login": True
#             }
#     except ArithmeticError as e:
#         logging.error(f"Internal server error: {e.args}")
#         return error_response(get_message("internal_server", "internal"), 500)


@router.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    # token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id":  setting.GOOGLE_CLIENT_ID,
        "client_secret": setting.GOOGLE_CLIENT_SECRET,
        "redirect_uri": setting.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    print(data,"*+++*+++*+++*+++*")
    response = requests.post(token_url, data=data)
    
    access_token = response.json().get("access_token")
    breakpoint()
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    return user_info.json()

@router.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, setting.GOOGLE_CLIENT_SECRET, algorithms=["HS256"])

