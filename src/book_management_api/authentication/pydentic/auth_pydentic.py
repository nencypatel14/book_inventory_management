from typing import Optional
from pydantic import BaseModel
# from src.book_management_api.user_information.pydantic.user_pydantic import UserDetails


class UserResponse(BaseModel):
    email: str
    id: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True

class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True
