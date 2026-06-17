from datetime import datetime

from fastapi import status

from app.core.security import get_pass_hash
from app.models.user import User


async def test_register(client, mock_db):
    payload = {
        "username": "Artemis",
        "email": "user@example.com",
        "password": "I_Love_You_3000!",
    }

    mock_db.execute.return_value.scalars.return_value.first.return_value = None

    async def mock_refresh(instance, attribute_names=None):
        instance.id = 99
        instance.created_at = datetime.utcnow()
        instance.updated_at = datetime.utcnow()

    mock_db.refresh.side_effect = mock_refresh

    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["username"] == "Artemis"
    assert data["id"] == 99
    assert data["email"] == "user@example.com"

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


async def test_login(client, mock_db):
    payload = {
        "username": "Artemis",
        "password": "I_Love_You_3000!",
    }

    test_user = User(
        id=99,
        username="Artemis",
        email="user@example.com",
        hashed_password=get_pass_hash("I_Love_You_3000!"),
    )

    mock_db.execute.return_value.scalars.return_value.first.return_value = test_user

    response = await client.post("/api/v1/auth/login", data=payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_register_fail(client, mock_db):
    payload = {
        "username": "Artemis",
        "email": "123",
        "password": "I_Love_You_3000!",
    }

    async def mock_refresh(instance, attribute_names=None):
        instance.id = 99
        instance.created_at = datetime.utcnow()
        instance.updated_at = datetime.utcnow()

    mock_db.refresh.side_effect = mock_refresh

    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_login_fail_unauthorized(client, mock_db):
    payload = {
        "username": "Artemis",
        "password": "I_Love_You_3000!",
    }

    test_user = User(
        id=99,
        username="Artemis",
        email="user@example.com",
        hashed_password=get_pass_hash("I_Love_You_4000!"),
    )

    mock_db.execute.return_value.scalars.return_value.first.return_value = test_user

    response = await client.post("/api/v1/auth/login", data=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
