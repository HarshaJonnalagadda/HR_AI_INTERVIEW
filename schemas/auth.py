from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str = "hr_manager"
    department: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(BaseModel):
    user: dict

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict
