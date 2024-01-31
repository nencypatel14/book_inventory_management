from pydantic import BaseModel
from typing import Optional

class UserDetails(BaseModel):
    username: str
    password: str
    role: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True


class UserDetailResponse(BaseModel):
    username: str
    role: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True


class UpdateUserInformation(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True
        str_strip_whitespace = True
