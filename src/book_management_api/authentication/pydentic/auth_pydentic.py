from pydantic import BaseModel, Field


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

class updatePassword(BaseModel):
    oldPassword: str
    newPassword: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True

class resetPassword(BaseModel):
    token: str
    password: str
    email: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True
