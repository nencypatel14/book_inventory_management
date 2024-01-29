from fastapi import APIRouter

from .book_route import router as router_book

router = APIRouter()

router.include_router(router_book)