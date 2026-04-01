import pytest


@pytest.mark.asyncio
async def test_save_onboarding_progress_success(client):
    create_payload = {
        "first_name": "Vincent",
        "last_name": "Moyaki",
        "phone_number": "+2348000000000",
    }

    await client.post("/api/v1/parents/me", json=create_payload)

    onboarding_payload = {
        "onboarding_step": 2,
        "country": "Nigeria",
        "state": "Lagos",
        "city": "Lagos",
        "address_line_1": "Lekki Phase 1",
    }

    response = await client.patch("/api/v1/parents/me/onboarding", json=onboarding_payload)

    assert response.status_code == 200
    data = response.json()

    assert data["onboarding_step"] == 2
    assert data["country"] == "Nigeria"
    assert data["state"] == "Lagos"
    assert data["city"] == "Lagos"


@pytest.mark.asyncio
async def test_save_onboarding_invalid_step_transition(client):
    create_payload = {
        "first_name": "Vincent",
        "last_name": "Moyaki",
        "phone_number": "+2348000000000",
    }

    await client.post("/api/v1/parents/me", json=create_payload)

    onboarding_payload = {
        "onboarding_step": 4,
        "country": "Nigeria",
    }

    response = await client.patch("/api/v1/parents/me/onboarding", json=onboarding_payload)

    assert response.status_code == 422
    assert "Invalid onboarding step transition" in response.json()["detail"]


@pytest.mark.asyncio
async def test_complete_onboarding_fails_when_required_fields_missing(client):
    create_payload = {
        "first_name": "Vincent",
        "last_name": "Moyaki",
        "phone_number": "+2348000000000",
    }

    await client.post("/api/v1/parents/me", json=create_payload)

    response = await client.post("/api/v1/parents/me/onboarding/complete")

    assert response.status_code == 422
    assert "Missing required fields" in response.json()["detail"]


@pytest.mark.asyncio
async def test_complete_onboarding_success(client):
    create_payload = {
        "first_name": "Vincent",
        "last_name": "Moyaki",
        "phone_number": "+2348000000000",
    }

    await client.post("/api/v1/parents/me", json=create_payload)

    onboarding_payload = {
        "onboarding_step": 2,
        "country": "Nigeria",
        "state": "Lagos",
        "city": "Lagos",
    }

    await client.patch("/api/v1/parents/me/onboarding", json=onboarding_payload)

    response = await client.post("/api/v1/parents/me/onboarding/complete")

    assert response.status_code == 200
    data = response.json()

    assert data["onboarding_completed"] is True
    assert data["message"] == "Parent onboarding completed successfully."