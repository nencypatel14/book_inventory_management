from pydantic import BaseModel


class AuthorDetail(BaseModel):
    first_name: str
    last_name: str
    email_id: str

    class Config:
        from_attributes = True
        str_strip_whitespace = True
