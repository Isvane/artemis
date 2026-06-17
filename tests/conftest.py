from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.deps import get_current_user
from app.database.connection import get_db
from app.main import app as fastapi_app
from app.models.project import Job, Project  # noqa: F401
from app.models.user import User  # noqa: F401

MOCK_LOGGED_IN_USER = User(id=99, username="Artemis", email="user@example.com")


@pytest.fixture(autouse=True)
def setup_auth_override():
    fastapi_app.dependency_overrides[get_current_user] = lambda: MOCK_LOGGED_IN_USER
    yield
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def mock_db():
    session = AsyncMock()
    session.add = MagicMock()
    mock_result = MagicMock()
    mock_result.scalar.return_value = 1
    session.execute.return_value = mock_result
    return session


@pytest.fixture
async def client(mock_db):
    async def _get_db_override():
        yield mock_db

    fastapi_app.dependency_overrides[get_db] = _get_db_override

    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        yield ac

    fastapi_app.dependency_overrides.clear()
