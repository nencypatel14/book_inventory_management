import logging
from fastapi import APIRouter, Depends, Security
from fastapi.encoders import jsonable_encoder
from config.config import setting

from database.db import Session, get_db
from src.general.constant import ADMIN
from src.general.dependencies import verifyToken
from src.book_management_api.user_information.pydantic.user_pydantic import UserDetails, UpdateUserInformation
from src.general.email import send_email
from src.general.response import error_response, get_message, success_response
from src.book_management_api.user_information.CRUD import user_CRUD as CRUDuser

router = APIRouter()

@router.post("/signup")
def create_account(user_info: UserDetails, db: Session = Depends(get_db)):
    """
    Sign up with provided input data.
    """
    try:
        existing_user = CRUDuser.get_user_by_username(db, user_info.username)

        if existing_user:
            return error_response("This Username already exists")
        
        account_detail = CRUDuser.user_signup(db, user_info)
        user_data = jsonable_encoder(account_detail)

        if user_info.role == "user":
            send_email(user_info.username, "User Signup Template", user_info.role)
        elif user_info.role == "admin":
            send_email(user_info.username, "Author Signup Template", user_info.role)

        # send_email(setting.MAIL_USERNAME, setting.MAIL_PASSWORD, user_info.username, user_info.role)

        return success_response(user_data, "User or Admin created successfully")
    except Exception as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)

@router.get("/list")
def get_user_information_list(db: Session = Depends(get_db), user: dict = Security(verifyToken, scopes=[ADMIN])):
    """
    Returns all user information.
    """
    try:
        if (user["scopes"][0] != ADMIN):
            return error_response("You are not allowed to get list of user information")
        
        user_information = CRUDuser.get_information(db)
        return success_response(user_information, "User information retrieved Successfully")
    except Exception as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)

@router.delete("/delete-user/{user_id}")
def delete_user(user_id:str, db: Session = Depends(get_db), user: dict = Security(verifyToken, scopes=[ADMIN])):
    """
    Delete User Detail in the database
    """
    try:
        if (user["scopes"][0] != ADMIN):
            return error_response("You are not allowed to delete user information.")

        existing_user = CRUDuser.get_user_details_by_id(db, user_id)

        if existing_user is None:
            return error_response("This User is not exist in database")
        
        deleteUser = CRUDuser.delete_user_information(db, user_id)

        if deleteUser <= 0:
            return {"message: No User found"}
        return success_response(None, "The requested User has been deleted Successfully")
    
    except Exception as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)
    
@router.put("/update/{input_user_id}")
def update_user_information(input_user_id: str, updateUsers: UpdateUserInformation, db: Session = Depends(get_db),  user: dict = Security(verifyToken, scopes=[ADMIN])):
    """
    Update user Information in the database by provided details .
    """
    try:
        if (user["scopes"][0] != ADMIN):
            return error_response("You are not allowed to delete user information.")

        existing_user = CRUDuser.get_user_details_by_id(db, input_user_id)
        if existing_user is None:
            return error_response("This User is not exist in database")

        update_users_information = CRUDuser.update_user(db, input_user_id, updateUsers)

        return success_response(update_users_information, "User Updated Successfully")
    except Exception as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)
    