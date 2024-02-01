import random
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.model import book_management_model as Table
from src.book_management_api.book_information.pydantic.book_pydantic import BookDetail, UpdateBookDetail, BookRate, UpdateBookReview

# Get List of all Book
def get_book_information(db: Session):
    return db.query(Table.BookInformation).all()

# Generate Rendom ISBN number
def generate_isbn():

    isbn12 = [random.randint(0, 9) for _ in range(12)]
    check_digit = (10 - sum((i + 1) * digit for i, digit in enumerate(isbn12)) % 10) % 10
    isbn13 = isbn12 + [check_digit]

    return ''.join(map(str, isbn13))

# Create Book Information in database
def create_book_information(db: Session, book: BookDetail):
    book_data = Table.BookInformation(
        id = uuid4(),
        title_name = book.title_name,
        author_id = book.author_id,
        publication_year = book.publication_year,
        genre = book.genre,
        ISBN = generate_isbn(),
        price = book.price
    )
    
    db.add(book_data)
    db.commit()
    db.refresh(book_data)
    return book_data

# Delete User From Database
def delete_user_information(db: Session, book_ID: str):
    deleted_book= db.query(
        Table.BookInformation
    ).filter(
        Table.BookInformation.id == book_ID
    ).delete()

    db.commit()
    return deleted_book

# Get Book Information From Database by Provided  book_id
def get_book_details_by_id(db:Session, book_id: str):
    data = db.query(
        Table.BookInformation
    ).filter(
        Table.BookInformation.id == book_id
    ).first()
    
    return data

# Update book Details in the database
def update_book_data(db: Session, update_book: UpdateBookDetail, book_id: str):
    current_book_detail = db.query(
        Table.BookInformation
    ).filter(
        Table.BookInformation.id == book_id
    ).first()

    if update_book.title_name:
        current_book_detail.title_name = update_book.title_name
    if update_book.author_id:
        current_book_detail.author_id = update_book.author_id
    if update_book.publication_year:
        current_book_detail.publication_year = update_book.publication_year
    if update_book.genre:
        current_book_detail.genre = update_book.genre
    if update_book.price:
        current_book_detail.price = update_book.price

    db.commit()
    db.refresh(current_book_detail)
    return current_book_detail

# Give Rating for Book 
def add_rating_of_book(db:  Session, rate: BookRate, id: str, bookId: str, book_review: str):
    book_data = Table.BookReviews(
        id = uuid4(),
        user_id = id,
        rating = rate.rating,
        book_id = bookId,
        review = book_review
    )
    
    db.add(book_data)
    db.commit()
    db.refresh(book_data)
    return book_data

# Update Rating in Database
def update_rating(db: Session, update_rate: UpdateBookReview, book_ID: str, user_ID: str):
    current_book_rating = db.query(
        Table.BookReviews
    ).filter(
        Table.BookReviews.book_id == book_ID,
        Table.BookReviews.user_id == user_ID
    ).first()

    if user_ID:
        current_book_rating.user_id = user_ID
    if update_rate.rating:
        current_book_rating.rating = update_rate.rating
    if update_rate.review:
        current_book_rating.review = update_rate.review

    db.commit()
    db.refresh(current_book_rating)
    return current_book_rating

# Get Rating by book_id and use
def get_rating_by_user_and_book(db: Session, user_ID: str, book_ID: str):
    data = db.query(
        Table.BookReviews
    ).filter(
        Table.BookReviews.book_id == book_ID,
        Table.BookReviews.user_id == user_ID
    ).first()
    
    return data

# Search Book Information by Author Name
def get_author_by_name(db: Session, search: str):
    author_by_name = db.query(
        Table.AuthorDetail
    ).filter(
        func.concat(Table.AuthorDetail.first_name, ' ', Table.AuthorDetail.last_name).ilike(f'%{search}%')
    ).first()

    return author_by_name

# Get Book Information By Author Id
def get_books_by_author_id(db: Session, author_id: int):
    book_by_id = db.query(
        Table.BookInformation
    ).filter(
        Table.BookInformation.author_id == author_id
    ).all()

    return book_by_id
