# backend/app/api/content.py
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from ..models.content import Content  # Relative import
from ..services.content import ContentService  # Relative import 
from ..database import Database  # Relative import

router = APIRouter()

@router.post("/", response_model=Content)
async def create_content(content: Content):
    try:
        db = await Database.connect_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database connection failed")
        service = ContentService(db)
        return await service.create(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{content_id}", response_model=Content)
async def get_content(content_id: str):
    try:
        db = await Database.connect_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database connection failed")
        service = ContentService(db)
        content = await service.get(content_id)
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Content])
async def list_contents(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    tags: Optional[List[str]] = Query(None),
    status: Optional[str] = Query(None, pattern="^(draft|published|archived)$")
):
    try:
        db = await Database.connect_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database connection failed")
        service = ContentService(db)
        filters = {}
        if tags:
            filters["tags"] = {"$in": tags}
        if status:
            filters["status"] = status
        return await service.list(skip=skip, limit=limit, filters=filters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{content_id}", response_model=Content)
async def update_content(content_id: str, content: Content):
    try:
        db = await Database.connect_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database connection failed")
        service = ContentService(db)
        updated = await service.update(content_id, content)
        if not updated:
            raise HTTPException(status_code=404, detail="Content not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{content_id}", status_code=204)
async def delete_content(content_id: str):
    try:
        db = await Database.connect_db()
        if not db:
            raise HTTPException(status_code=503, detail="Database connection failed")
        service = ContentService(db)
        deleted = await service.delete(content_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Content not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))