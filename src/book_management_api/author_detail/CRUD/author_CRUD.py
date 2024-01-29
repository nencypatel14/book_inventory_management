from uuid import uuid4
from sqlalchemy.orm import Session

from src.model import book_management_model as Table
from src.book_management_api.author_detail.pydentic.author_pydentic import AuthorDetail

def Create_author_detail(db: Session, author: AuthorDetail):
    author_data = Table.AuthorDetail(
        id = uuid4(),
        first_name = author.first_name,
        last_name = author.last_name,
        email_id = author.email_id
    )
    db.add(author_data)
    db.commit()
    db.refresh(author_data)
    return author_data

def get_user_by_email(db:Session, email: str):
    data = db.query(
        Table.AuthorDetail
    ).filter(
        Table.AuthorDetail.email_id == email
    ).first()
    
    return data