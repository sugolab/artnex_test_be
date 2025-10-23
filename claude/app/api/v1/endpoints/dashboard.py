"""
Dashboard API Endpoints
Main dashboard, brand shortcuts, user status, and search
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.brand import Brand, BrandKPI
from app.schemas.dashboard import (
    DashboardResponse,
    BrandShortcut,
    UserStatus,
    AIRecommendation,
    BrandSearchRequest,
    BrandSearchResponse
)

router = APIRouter()


@router.get("/", response_model=DashboardResponse, summary="Get Main Dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> DashboardResponse:
    """
    Get main dashboard data for logged-in user

    Returns:
        DashboardResponse: Dashboard data including brand shortcuts, user status, and AI recommendations
    """
    # Get brand shortcuts (registered brands with latest KPIs)
    brands_query = select(Brand).where(
        Brand.user_id == current_user.id,
        Brand.status == "active"
    ).order_by(desc(Brand.updated_at)).limit(10)

    brands_result = await db.execute(brands_query)
    brands = brands_result.scalars().all()

    brand_shortcuts = []
    for brand in brands:
        # Get latest KPI for each brand
        kpi_query = select(BrandKPI).where(
            BrandKPI.brand_id == brand.id
        ).order_by(desc(BrandKPI.measurement_date)).limit(1)

        kpi_result = await db.execute(kpi_query)
        latest_kpi = kpi_result.scalar_one_or_none()

        brand_shortcuts.append(BrandShortcut(
            id=brand.id,
            brand_name=brand.brand_name,
            category=brand.category,
            logo_url=brand.logo_url,
            latest_kpi=latest_kpi.value if latest_kpi else None,
            kpi_trend="stable",  # TODO: Calculate trend based on historical data
            updated_at=brand.updated_at
        ))

    # Get user status
    total_brands_query = select(func.count(Brand.id)).where(
        Brand.user_id == current_user.id
    )
    total_brands_result = await db.execute(total_brands_query)
    total_brands = total_brands_result.scalar()

    user_status = UserStatus(
        subscription_status=current_user.subscription_status,
        is_verified=current_user.is_verified,
        total_brands=total_brands or 0,
        total_campaigns=0,  # TODO: Add campaigns count when Campaign model is ready
        last_login=current_user.last_login
    )

    # AI recommendations (mock for now)
    ai_recommendations = [
        AIRecommendation(
            brand_name="추천 브랜드 1",
            category="뷰티",
            reason="20대 여성 타깃 트렌드 증가",
            confidence_score=0.85
        )
    ]

    return DashboardResponse(
        welcome_message=f"안녕하세요, {current_user.name}님! 👋",
        brand_shortcuts=brand_shortcuts,
        user_status=user_status,
        ai_recommendations=ai_recommendations,
        recent_activity=[]
    )


@router.get("/brands/shortcuts", response_model=List[BrandShortcut], summary="Get Brand Shortcuts")
async def get_brand_shortcuts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 10
) -> List[BrandShortcut]:
    """
    Get brand shortcuts (quick access cards) for dashboard

    Args:
        limit: Maximum number of brands to return (default: 10)

    Returns:
        List[BrandShortcut]: List of brand shortcut cards
    """
    brands_query = select(Brand).where(
        Brand.user_id == current_user.id,
        Brand.status == "active"
    ).order_by(desc(Brand.updated_at)).limit(limit)

    brands_result = await db.execute(brands_query)
    brands = brands_result.scalars().all()

    shortcuts = []
    for brand in brands:
        kpi_query = select(BrandKPI).where(
            BrandKPI.brand_id == brand.id
        ).order_by(desc(BrandKPI.measurement_date)).limit(1)

        kpi_result = await db.execute(kpi_query)
        latest_kpi = kpi_result.scalar_one_or_none()

        shortcuts.append(BrandShortcut(
            id=brand.id,
            brand_name=brand.brand_name,
            category=brand.category,
            logo_url=brand.logo_url,
            latest_kpi=latest_kpi.value if latest_kpi else None,
            kpi_trend="stable",
            updated_at=brand.updated_at
        ))

    return shortcuts


@router.get("/user/status", response_model=UserStatus, summary="Get User Status")
async def get_user_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserStatus:
    """
    Get current user status and subscription information

    Returns:
        UserStatus: User status including subscription and usage statistics
    """
    total_brands_query = select(func.count(Brand.id)).where(
        Brand.user_id == current_user.id
    )
    total_brands_result = await db.execute(total_brands_query)
    total_brands = total_brands_result.scalar()

    return UserStatus(
        subscription_status=current_user.subscription_status,
        is_verified=current_user.is_verified,
        total_brands=total_brands or 0,
        total_campaigns=0,
        last_login=current_user.last_login
    )


@router.post("/search/brands", response_model=BrandSearchResponse, summary="Search Brands with AI Recommendations")
async def search_brands(
    search_request: BrandSearchRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BrandSearchResponse:
    """
    Search brands with AI-powered recommendations

    Args:
        search_request: Search query and filters

    Returns:
        BrandSearchResponse: Search results with AI suggestions
    """
    # Build search query
    query = select(Brand).where(Brand.user_id == current_user.id)

    # Apply search filter
    if search_request.query:
        query = query.where(
            Brand.brand_name.ilike(f"%{search_request.query}%")
        )

    # Apply category filter
    if search_request.category:
        query = query.where(Brand.category == search_request.category)

    # Apply limit and ordering
    query = query.order_by(desc(Brand.updated_at)).limit(search_request.limit)

    # Execute query
    result = await db.execute(query)
    brands = result.scalars().all()

    # Get total count
    count_query = select(func.count(Brand.id)).where(Brand.user_id == current_user.id)
    if search_request.query:
        count_query = count_query.where(
            Brand.brand_name.ilike(f"%{search_request.query}%")
        )
    count_result = await db.execute(count_query)
    total_count = count_result.scalar()

    # Convert to shortcuts
    shortcuts = []
    for brand in brands:
        kpi_query = select(BrandKPI).where(
            BrandKPI.brand_id == brand.id
        ).order_by(desc(BrandKPI.measurement_date)).limit(1)

        kpi_result = await db.execute(kpi_query)
        latest_kpi = kpi_result.scalar_one_or_none()

        shortcuts.append(BrandShortcut(
            id=brand.id,
            brand_name=brand.brand_name,
            category=brand.category,
            logo_url=brand.logo_url,
            latest_kpi=latest_kpi.value if latest_kpi else None,
            kpi_trend="stable",
            updated_at=brand.updated_at
        ))

    # AI suggestions (mock for now - will integrate GPT API later)
    ai_suggestions = [
        AIRecommendation(
            brand_name=f"{search_request.query} 유사 브랜드",
            category=search_request.category or "일반",
            reason="검색어 기반 AI 추천",
            confidence_score=0.75
        )
    ]

    return BrandSearchResponse(
        brands=shortcuts,
        ai_suggestions=ai_suggestions,
        total_count=total_count or 0
    )
