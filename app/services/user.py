# backend/app/services/user.py
from typing import Optional
from app.models.user import User
from .base import BaseService

class UserService(BaseService[User]):
    def __init__(self, db):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        doc = await self.collection.find_one({"email": email})
        return User(**doc) if doc else None

    async def update_status(self, id: str, disabled: bool) -> Optional[User]:
        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"disabled": disabled}}
        )
        return await self.get(id) if result.modified_count else None