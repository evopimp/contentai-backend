# backend/app/models/user.py
from typing import Optional
from .base import MongoBaseModel
from pydantic import EmailStr, Field

class User(MongoBaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    disabled: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe"
            }
        }