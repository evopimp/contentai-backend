# backend/tests/test_services.py
import pytest
from bson import ObjectId
from app.models.content import Content
from app.models.user import User
from app.services.content import ContentService
from app.services.user import UserService
from app.database import Database

@pytest.fixture
async def db():
    database = await Database.connect_db()
    yield database
    # Cleanup collections after tests
    await database.content.delete_many({})
    await database.user.delete_many({})

@pytest.fixture
def test_content():
    return Content(
        title="Test Content",
        description="Test Description",
        content_type="article",
        tags=["test", "pytest"]
    )

@pytest.fixture
def test_user():
    return User(
        email="test@example.com",
        username="testuser"
    )

@pytest.mark.asyncio
class TestContentService:
    async def test_create_content(self, db, test_content):
        service = ContentService(db)
        content = await service.create(test_content)
        assert content.id is not None
        assert content.title == test_content.title

    async def test_get_content(self, db, test_content):
        service = ContentService(db)
        created = await service.create(test_content)
        retrieved = await service.get(str(created.id))
        assert retrieved is not None
        assert retrieved.title == test_content.title

    async def test_search_by_tags(self, db, test_content):
        service = ContentService(db)
        await service.create(test_content)
        results = await service.search_by_tags(["test"])
        assert len(results) > 0
        assert results[0].tags == test_content.tags

    async def test_update_status(self, db, test_content):
        service = ContentService(db)
        content = await service.create(test_content)
        updated = await service.update_status(str(content.id), "published")
        assert updated.status == "published"

@pytest.mark.asyncio
class TestUserService:
    async def test_create_user(self, db, test_user):
        service = UserService(db)
        user = await service.create(test_user)
        assert user.id is not None
        assert user.email == test_user.email

    async def test_get_by_email(self, db, test_user):
        service = UserService(db)
        await service.create(test_user)
        user = await service.get_by_email(test_user.email)
        assert user is not None
        assert user.email == test_user.email

    async def test_update_status(self, db, test_user):
        service = UserService(db)
        user = await service.create(test_user)
        updated = await service.update_status(str(user.id), True)
        assert updated.disabled is True