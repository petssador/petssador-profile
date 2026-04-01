import pytest


@pytest.mark.asyncio
async def test_update_parent_profile_success(client):
    create_payload = {
        "first_name": "Vincent",
        "last_name": "Moyaki",
        "phone_number": "+2348000000000",
    }

    await client.post("/api/v1/parents/me", json=create_payload)

    update_payload = {
        "country": "Nigeria",
        "state": "Lagos",
        "city": "Lagos",
        "preferred_contact_method": "phone",
    }

    response = await client.patch("/api/v1/parents/me", json=update_payload)

    assert response.status_code == 200
    data = response.json()

    assert data["country"] == "Nigeria"
    assert data["state"] == "Lagos"
    assert data["city"] == "Lagos"
    assert data["preferred_contact_method"] == "phone"


@pytest.mark.asyncio
async def test_update_parent_profile_not_found(client):
    response = await client.patch(
        "/api/v1/parents/me",
        json={"city": "Lagos"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Parent profile not found."