from uuid import uuid4
import bcrypt
from sqlalchemy.orm import Session

from src.model import book_management_model as Table
from src.book_management_api.user_information.pydantic.user_pydantic import UpdateUserInformation, UserDetails


def user_signup(db: Session, user: UserDetails):
    hashedPassword = bcrypt.hashpw(
        user.password.strip().encode("utf-8"), bcrypt.gensalt(rounds=12)
    )
    password_hash = hashedPassword.decode("utf-8")
    user_info = Table.UserInformation(
        id = uuid4(),
        username = user.username,
        password = password_hash,
        role = user.role
    )
    db.add(user_info)
    db.commit()
    db.refresh(user_info)
    return user_info


def get_information(db: Session):
    return db.query(Table.UserInformation).all()


def get_user_details_by_id(db:Session, user_id: str):
    data = db.query(
        Table.UserInformation
    ).filter(
        Table.UserInformation.id == user_id
    ).first()
    
    return data


def delete_user_information(db: Session, user_ID: str):
    deleted_user= db.query(
        Table.UserInformation
    ).filter(
        Table.UserInformation.id == user_ID
    ).delete()

    db.commit()
    return deleted_user


def update_user(db: Session, user_id: str, updateUser: UpdateUserInformation):
    current_user = db.query(
        Table.UserInformation
    ).filter(
        Table.UserInformation.id == user_id
    ).first()
    
    if updateUser.username:
        current_user.username = updateUser.username
    if updateUser.role:
        current_user.role = updateUser.role
    db.commit()
    db.refresh(current_user)
    return current_user


def get_user_by_username(db:Session, username: str):
    data = db.query(
        Table.UserInformation
    ).filter(
        Table.UserInformation.username == username
    ).first()
    
    return data