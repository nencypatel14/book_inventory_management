from fastapi import APIRouter

from src.book_management_api.authentication.endpoint import auth_endpoint
from src.book_management_api.user_information.endpoint import user_endpoint
from src.book_management_api.book_information.endpoint import book_endpoint
from src.book_management_api.author_detail.endpoint import author_endpoint

router = APIRouter(prefix="/book")

router.include_router(auth_endpoint.router, prefix="/login", tags=["Authentication"])
router.include_router(user_endpoint.router, prefix="/user-information", tags=["Users Information"])
router.include_router(book_endpoint.router, prefix="/book-information", tags=["Book Information"])
router.include_router(author_endpoint.router, prefix="/author-infomation", tags=["Author Information"])
