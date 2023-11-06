from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    dob: date
    gender: str
    university: Optional[str]
    mobile: Optional[str]
    country: Optional[str]
