# app/services/content.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.content import Content
from datetime import datetime
from typing import List, Optional

class ContentService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.contents

    async def create(self, content: Content) -> Content:
        content_dict = content.model_dump(exclude_unset=True)
        result = await self.collection.insert_one(content_dict)
        content.id = str(result.inserted_id)
        return content

    async def get(self, content_id: str) -> Optional[Content]:
        content = await self.collection.find_one({"_id": content_id})
        return Content(**content) if content else None

    async def list(self, skip: int = 0, limit: int = 10) -> List[Content]:
        cursor = self.collection.find().skip(skip).limit(limit)
        contents = await cursor.to_list(length=limit)
        return [Content(**content) for content in contents]

    async def update(self, content_id: str, content: Content) -> Optional[Content]:
        content.updated_at = datetime.utcnow()
        update_data = content.model_dump(exclude_unset=True)
        result = await self.collection.update_one(
            {"_id": content_id},
            {"$set": update_data}
        )
        return await self.get(content_id) if result.modified_count else None