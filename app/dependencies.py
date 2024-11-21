# app/dependencies.py
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import Database

async def get_database() -> AsyncIOMotorDatabase:
    return await Database.connect_db()