# backend/app/services/base.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from bson import ObjectId

T = TypeVar('T', bound=BaseModel)

class BaseService(Generic[T]):
    def __init__(self, db: AsyncIOMotorDatabase, model: type[T]):
        self.db = db
        self.model = model
        self.collection = db[model.__name__.lower()]

    async def create(self, item: T) -> T:
        doc = item.model_dump(exclude_unset=True)
        result = await self.collection.insert_one(doc)
        return await self.get(result.inserted_id)

    async def get(self, id: str) -> Optional[T]:
        doc = await self.collection.find_one({"_id": ObjectId(id)})
        return self.model(**doc) if doc else None

    async def list(self, skip: int = 0, limit: int = 10) -> List[T]:
        cursor = self.collection.find().skip(skip).limit(limit)
        return [self.model(**doc) async for doc in cursor]