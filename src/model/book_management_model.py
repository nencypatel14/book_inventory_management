from sqlalchemy import Column, Float, ForeignKey, String, DateTime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from database.db import Base

class UserInformation(Base):
    __tablename__ = "user_information"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    username = Column(String(length=200), nullable=False)
    password = Column(String(length=255), nullable=False)
    role = Column(String(length=50), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow())
    modified_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())


class BookInformation(Base):
    __tablename__ = "book_information"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    title_name = Column(String(length=255), nullable=False)
    author_id = Column(UUID, ForeignKey('author_detail.id'))
    publication_year = Column(String, nullable=False)
    genre = Column(String(length=255), nullable=False)
    ISBN = Column(String(length=13), nullable=True)
    price = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow())
    modified_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())


class BookReviews(Base):
    __tablename__ = "book_review"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_id = Column(UUID, ForeignKey('user_information.id'))
    book_id = Column(UUID, ForeignKey('book_information.id'))
    review = Column(String(length=255))
    rating = Column(String(length=100))

    created_at = Column(DateTime, default=datetime.utcnow())
    modified_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())


class AuthorDetail(Base):
    __tablename__= "author_detail"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=200), nullable=False)
    email_id = Column(String(length=200), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow())
    modified_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
