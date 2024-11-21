# backend/app/models/content.py
from typing import List, Optional
from .base import MongoBaseModel
from pydantic import Field, HttpUrl

class Content(MongoBaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    content_type: str = Field(..., pattern="^(article|video|audio|document)$")
    tags: List[str] = Field(default_factory=list)
    url: Optional[HttpUrl] = None
    status: str = Field(default="draft", pattern="^(draft|published|archived)$")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Getting Started with AI",
                "description": "A beginner's guide to AI",
                "content_type": "article",
                "tags": ["AI", "beginners", "guide"],
                "status": "draft"
            }
        }