import logging
from fastapi import APIRouter, Depends, Security
from fastapi.encoders import jsonable_encoder

from database.db import get_db, Session
from src.general.constant import ADMIN, USER
from src.general.dependencies import verifyToken
from src.book_management_api.book_information.pydantic.book_pydantic import BookDetail, UpdateBookDetail, RatingEnum, BookRating
from src.general.response import get_message, error_response, success_response
from src.book_management_api.book_information.CRUD import book_CRUD as CRUDbook

router = APIRouter()

@router.get("/list")
def get_book_information_list(db: Session = Depends(get_db), user: dict = Security(verifyToken, scopes=[ADMIN])):
    """
    Returns all book information.
    """
    try:
        if (user["scopes"][0] != ADMIN):
            return error_response("You are not allowed to get list of book information")
        
        book_information = CRUDbook.get_book_information(db)
        return success_response(book_information, "Book Information retrieved Successfilly")
    
    except Exception as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)


@router.post("/add-book")
def add_book_details(input_data: BookDetail, db: Session = Depends(get_db), user: dict = Security(verifyToken, scopes=[ADMIN, USER])):
    """
    Add Book Details in the database with provided input data.
    """
    try:
        if(user["scopes"][0] not in [ADMIN, USER]):
            return error_response("You are not Allowed to add book Information")

        add_book = CRUDbook.create_book_information(db, input_data)
        return success_response(add_book, "Book Information created Successfully into the database")
     
    except Exception as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)
    

@router.delete("delete-book/{book_id}")
def delete_book_data(book_id: str, db: Session = Depends(get_db), user: dict = Security(verifyToken, scopes=[ADMIN])):
    """
    Delete book details in the database with provided book id.
    """
    try:
        if (user["scopes"][0] != ADMIN):
            return error_response("You are not allowed to delete book information.")

        existing_book = CRUDbook.get_book_details_by_id(db, book_id)

        if existing_book is None:
            return error_response("This book is not exist in database")
        
        deletebook = CRUDbook.delete_user_information(db, book_id)

        if deletebook <= 0:
            return {"message: No Book found"}
        return success_response(None, "The requested book has been deleted Successfully")
         
    except Exception as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)
    

@router.put("/update-book/{book_id}")
def update_book_detail(book_id: str, updateBook: UpdateBookDetail, db: Session = Depends(get_db)):
    """
    Update book Details in the database
    """
    try:
        existing_book_data = CRUDbook.get_book_details_by_id(db, book_id)

        if existing_book_data is None:
            return error_response("This book information is not exist in Database.")

        update_book = CRUDbook.update_book_data(db, updateBook, book_id)
        return success_response(update_book, "Book Information Updated Successfully")
    
    except Exception as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)
    

@router.post("/book-rating/{book_id}")
def add_book_rating(book_id: str, rating: RatingEnum, review: str, book_data = Depends(BookRating), db: Session = Depends(get_db),user: dict = Security(verifyToken, scopes=[USER])):
    """
    add book rating for input book data
    """
    try:
        if (user["scopes"][0] != USER):
            return error_response("You are not allowed to give rating on book.")

        existing_book_data = CRUDbook.get_book_details_by_id(db, book_id)

        if existing_book_data is None:
            return error_response("This book information is not exist in Database.")
        
        existing_rating = CRUDbook.get_rating_by_user_and_book(db, user["ID"], book_id)

        if existing_rating:
            updated_rate = CRUDbook.update_rating(db, book_data, book_id, user["ID"])
            return success_response(updated_rate, "Rating Updated Successfully")

        else:
            add_rating = CRUDbook.add_rating_of_book(db,book_data,user["ID"], book_id, review)
            return success_response(add_rating, "Rating Added Successfully")
    
    except ArithmeticError as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)


@router.post("/search-book")
def search_book(author_name: str, db: Session = Depends(get_db)):
    """
    Search book with using author name 
    """
    try:
        # Modify to use a single author_name parameter
        author = CRUDbook.get_author_by_name(db, author_name)

        if author is None:
            return error_response("This author information does not exist in the database.")

        books = CRUDbook.get_books_by_author_id(db, author.id)

        book_data = []
        for book in books:
            book_dict = jsonable_encoder(book)
            book_dict['author_id'] = author.id  # Use author.id instead of author_name
            book_data.append(book_dict)

        return success_response(book_data, "Fetch list of books successfully")
    except ValueError:
        return error_response("Invalid author name format. Please provide both first name and last name.")

