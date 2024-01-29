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


