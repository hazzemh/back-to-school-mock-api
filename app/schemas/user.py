from pydantic import BaseModel, EmailStr


class CurrentUser(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    display_name: str
    email: EmailStr
    role: str
    preferred_language: str = "en"


class UserInDB(CurrentUser):
    password_hash: str

