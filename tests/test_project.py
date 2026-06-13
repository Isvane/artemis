from datetime import datetime

from fastapi import status


async def test_create_project_success(client, mock_db):
    payload = {
        "name": "Artemis Launch Platform",
        "jobs": [{"status": "PENDING"}, {"status": "RUNNING"}],
    }

    async def mock_refresh(instance, attribute_names=None):
        instance.id = 99
        if hasattr(instance, "jobs"):
            for i, job in enumerate(instance.jobs):
                job.id = i + 1
                job.project_id = 99
                job.created_at = datetime.utcnow()

    mock_db.refresh.side_effect = mock_refresh

    response = await client.post("/api/v1/projects", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["name"] == "Artemis Launch Platform"
    assert data["id"] == 99
    assert len(data["jobs"]) == 2
    assert data["jobs"][0]["status"] == "PENDING"

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


async def test_create_project_invalid_payload(client):
    bad_payload = {"jobs": [{"status": "PENDING"}]}

    response = await client.post("/api/v1/projects", json=bad_payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    errors = response.json()["detail"]
    assert errors[0]["loc"] == ["body", "name"]
    assert errors[0]["type"] == "missing"
