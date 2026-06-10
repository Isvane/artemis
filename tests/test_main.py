from fastapi import status


async def test_root_endpoint(client):
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Goodbye World!"}


async def test_healthz_healthy(client, mock_db):
    response = await client.get("/healthz")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy", "database": "connected"}
    mock_db.execute.assert_called_once()


async def test_healthz_unhealthy(client, mock_db):
    """Tests /healthz when the database raises an exception."""
    mock_db.execute.side_effect = Exception("Connection timed out")

    response = await client.get("/healthz")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert "Database connection failed" in response.json()["detail"]
