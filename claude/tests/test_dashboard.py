"""
Dashboard API Tests
대시보드 API 테스트
"""
import pytest
from httpx import AsyncClient
from app.models.user import User
from app.models.brand import Brand


@pytest.mark.asyncio
async def test_get_dashboard_unauthorized(client: AsyncClient):
    """인증 없이 대시보드 접근 테스트"""
    response = await client.get("/api/v1/dashboard")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_dashboard_success(
    client: AsyncClient,
    auth_headers: dict,
    test_brand: Brand
):
    """대시보드 조회 성공 테스트"""
    response = await client.get(
        "/api/v1/dashboard",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "user" in data
    assert "ai_recommendations" in data
    assert "quick_actions" in data
    assert "recent_activity" in data


@pytest.mark.asyncio
async def test_get_brand_shortcuts(
    client: AsyncClient,
    auth_headers: dict,
    test_brand: Brand
):
    """브랜드 숏컷 조회 테스트"""
    response = await client.get(
        "/api/v1/dashboard/brands/shortcuts",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "brands" in data
    assert len(data["brands"]) > 0
    assert data["brands"][0]["brand_name"] == "Test Brand"


@pytest.mark.asyncio
async def test_get_user_status(
    client: AsyncClient,
    auth_headers: dict
):
    """사용자 상태 조회 테스트"""
    response = await client.get(
        "/api/v1/dashboard/user/status",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "subscription_status" in data
    assert "is_active" in data
    assert "total_brands" in data


@pytest.mark.asyncio
async def test_search_brands(
    client: AsyncClient,
    auth_headers: dict,
    test_brand: Brand
):
    """브랜드 검색 테스트"""
    response = await client.post(
        "/api/v1/dashboard/search/brands",
        headers=auth_headers,
        json={
            "query": "Test",
            "filters": {"category": "뷰티"}
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "results" in data
    assert "ai_suggestions" in data
