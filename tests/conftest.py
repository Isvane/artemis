from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.database.connection import get_db
from app.main import app as fastapi_app
from app.models.project import Job, Project  # noqa: F401
from app.models.user import User  # noqa: F401


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
