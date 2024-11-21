# app/tests/conftest.py
import pytest
from app.database import Database

@pytest.fixture(scope="session")
async def db():
    database = await Database.connect_db()
    yield database
    await database.client.close()