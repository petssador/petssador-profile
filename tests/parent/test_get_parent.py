import pytest


@pytest.mark.asyncio
async def test_get_parent_profile_success(client):
    payload = {
        "first_name": "Vincent",
        "last_name": "Moyaki",
        "phone_number": "+2348000000000",
    }

    await client.post("/api/v1/parents/me", json=payload)
    response = await client.get("/api/v1/parents/me")

    assert response.status_code == 200
    data = response.json()

    assert data["first_name"] == "Vincent"
    assert data["last_name"] == "Moyaki"


@pytest.mark.asyncio
async def test_get_parent_profile_not_found(client):
    response = await client.get("/api/v1/parents/me")

    assert response.status_code == 404
    assert response.json()["detail"] == "Parent profile not found."