import pytest


@pytest.mark.asyncio
async def test_create_parent_profile_success(client):
    payload = {
        "first_name": "Vincent",
        "last_name": "Moyaki",
        "phone_number": "+2348000000000",
    }

    response = await client.post("/api/v1/parents/me", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["first_name"] == "Vincent"
    assert data["last_name"] == "Moyaki"
    assert data["phone_number"] == "+2348000000000"
    assert data["onboarding_step"] == 1
    assert data["onboarding_completed"] is False
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_create_parent_profile_duplicate_returns_conflict(client):
    payload = {
        "first_name": "Vincent",
        "last_name": "Moyaki",
        "phone_number": "+2348000000000",
    }

    first_response = await client.post("/api/v1/parents/me", json=payload)
    second_response = await client.post("/api/v1/parents/me", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Parent profile already exists for this user."