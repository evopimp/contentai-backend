# backend/app/api/user.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.user import User
from app.services.user import UserService
from app.database import Database

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: User):
    db = await Database.connect_db()
    service = UserService(db)
    existing = await service.get_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await service.create(user)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    db = await Database.connect_db()
    service = UserService(db)
    user = await service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}/status", response_model=User)
async def update_user_status(user_id: str, disabled: bool):
    db = await Database.connect_db()
    service = UserService(db)
    user = await service.update_status(user_id, disabled)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user