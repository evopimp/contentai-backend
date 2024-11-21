# backend/tests/test_database.py
import pytest
from app.database import Database

@pytest.mark.asyncio
class TestDatabase:
    async def test_connection(self):
        db = await Database.connect_db()
        assert db is not None