from pydantic import BaseModel


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
