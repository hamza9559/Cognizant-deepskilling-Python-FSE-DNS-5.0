import pytest
from httpx import AsyncClient, ASGITransport
from fastapp.main import app

@pytest.mark.asyncio
async def test_get_courses_endpoint():
    """Assert that fetching seeded courses returns a successful response code"""
    # Updated constructor format using ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/courses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_course_unauthorized():
    """Assert that unauthorized anonymous posts without a JWT token get blocked with code 401"""
    # Updated constructor format using ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/courses/", json={
            "name": "Testing Architecture",
            "code": "TEST101",
            "credits": 3,
            "department_id": 1
        })
    assert response.status_code == 401