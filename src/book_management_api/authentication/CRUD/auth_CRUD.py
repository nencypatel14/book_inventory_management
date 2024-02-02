import bcrypt
from sqlalchemy.orm import Session
from src.model import book_management_model as Table


# Get user by email
def getUserByEmailID(db: Session, email: str):
    return (
        db.query(Table.UserInformation)
        .filter(Table.UserInformation.username == email)
        .first()
    )

# Verify password
def getVerifyPassword(db: Session, Password: str):
    return (
        db.query(Table.UserInformation)
        .filter(Table.UserInformation.password == Password)
        .first()
    )

def resetPasswordRequest(db: Session, email: str):
    user = db.query(Table.UserInformation
        ).filter(Table.UserInformation.username == email
        ).first()
    
    return user


def resetPassword(db: Session, email: str, new_password: str):
    hashedPassword = bcrypt.hashpw(
        new_password.strip().encode("utf-8"), bcrypt.gensalt(rounds=12)
    )
    # password_hash = hashedPassword.decode("utf-8")
    user = db.query(Table.UserInformation
        ).filter(Table.UserInformation.username == email
        ).first()
    user.password = hashedPassword.decode("utf-8")
    
    db.commit()
    db.refresh(user)

    return user