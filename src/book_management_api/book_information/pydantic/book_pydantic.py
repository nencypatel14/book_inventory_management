from enum import Enum
from pydantic import BaseModel
from typing import Optional


class BookDetail(BaseModel):
    title_name: str
    author_id: str
    publication_year: str
    genre: str
    ISBN: str = None
    price: float

    class Config:
        from_attributes = True
        str_strip_whitespace = True

class UpdateBookDetail(BaseModel):
    title_name: Optional[str] = None
    author_id: Optional[str] = None
    publication_year: Optional[str] = None
    genre: Optional[str] = None
    ISBN: Optional[str] = None
    price: Optional[float] = None

    class Config:
        from_attributes = True
        str_strip_whitespace = True


class BookRate(BaseModel):
    user_id: str = None
    rating: str
    book_id: str
    review: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True


class UpdateBookReview(BaseModel):
    user_id: Optional[str] = None
    rating: Optional[str] 
    book_id: Optional[str]
    review: Optional[str]

    class Config:
        from_attributes = True
        str_strip_whitespace = True


class RatingEnum(str, Enum):
    one_star = "1"
    two_star = "2"
    three_star = "3"
    four_star = "4"
    five_star = "5"


class BookRating:
    def __init__(self, book_id: str, rating: RatingEnum, review: str):
        self.book_id = book_id
        self.rating = rating
        self.review = review
