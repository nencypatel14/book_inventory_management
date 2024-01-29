import logging
from fastapi import APIRouter, Depends

from database.db import get_db, Session
from src.general.response import error_response, get_message, success_response
from src.book_management_api.author_detail.CRUD import author_CRUD as CRUDauthor
from src.book_management_api.author_detail.pydentic.author_pydentic import AuthorDetail

router = APIRouter()

@router.post("/add-author")
def add_author_detail(input_data: AuthorDetail, db: Session = Depends(get_db)):
    """
    Add author Information in the database with provied Data.
    """
    try:
        existing_author = CRUDauthor.get_user_by_email(db, input_data.email_id)

        if existing_author:
            return error_response("This Email ID already exists")

        add_author = CRUDauthor.Create_author_detail(db, input_data)
        return success_response(add_author, "Author Created Successfully.")
    
    except Exception as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)
    