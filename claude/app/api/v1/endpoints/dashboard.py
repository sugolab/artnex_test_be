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
from app.services.gpt_service import gpt_service
from app.services.kpi_service import kpi_service

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

        # Calculate KPI trend using KPI service
        kpi_trend = await kpi_service.get_kpi_trend(db, brand.id, "popularity_index", 30)

        brand_shortcuts.append(BrandShortcut(
            id=brand.id,
            brand_name=brand.brand_name,
            category=brand.category,
            logo_url=brand.logo_url,
            latest_kpi=latest_kpi.value if latest_kpi else None,
            kpi_trend=kpi_trend,
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

    # AI recommendations using GPT API
    ai_recommendations = []

    # Get AI recommendations if user has brands or interests
    if total_brands > 0:
        # Get user's brand categories for personalized recommendations
        categories_query = select(Brand.category).where(
            Brand.user_id == current_user.id
        ).distinct().limit(3)
        categories_result = await db.execute(categories_query)
        user_categories = [cat for cat in categories_result.scalars().all() if cat]

        # Generate AI recommendations for each category
        for category in user_categories[:2]:  # Limit to 2 categories to save tokens
            gpt_result = await gpt_service.recommend_brands(
                industry=category,
                target_audience="제조업 브랜드 담당자",
                limit=1
            )

            if gpt_result["success"] and gpt_result["data"]:
                recommendations = gpt_result["data"].get("recommendations", [])
                for rec in recommendations[:1]:  # Take only first recommendation
                    ai_recommendations.append(AIRecommendation(
                        brand_name=rec.get("brand_name", "AI 추천 브랜드"),
                        category=category,
                        reason=rec.get("differentiation", "AI 기반 추천"),
                        confidence_score=0.85
                    ))

    # Default recommendation if no personalized ones
    if not ai_recommendations:
        ai_recommendations = [
            AIRecommendation(
                brand_name="AI 브랜드 추천",
                category="일반",
                reason="브랜드를 등록하면 맞춤형 AI 추천을 받을 수 있습니다",
                confidence_score=0.5
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

        # Calculate KPI trend using KPI service
        kpi_trend = await kpi_service.get_kpi_trend(db, brand.id, "popularity_index", 30)

        shortcuts.append(BrandShortcut(
            id=brand.id,
            brand_name=brand.brand_name,
            category=brand.category,
            logo_url=brand.logo_url,
            latest_kpi=latest_kpi.value if latest_kpi else None,
            kpi_trend=kpi_trend,
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

        # Calculate KPI trend using KPI service
        kpi_trend = await kpi_service.get_kpi_trend(db, brand.id, "popularity_index", 30)

        shortcuts.append(BrandShortcut(
            id=brand.id,
            brand_name=brand.brand_name,
            category=brand.category,
            logo_url=brand.logo_url,
            latest_kpi=latest_kpi.value if latest_kpi else None,
            kpi_trend=kpi_trend,
            updated_at=brand.updated_at
        ))

    # AI suggestions using GPT API
    ai_suggestions = []

    # Generate AI suggestions based on search query
    if search_request.query or search_request.category:
        gpt_result = await gpt_service.recommend_brands(
            industry=search_request.category or "일반",
            keywords=[search_request.query] if search_request.query else None,
            limit=3
        )

        if gpt_result["success"] and gpt_result["data"]:
            recommendations = gpt_result["data"].get("recommendations", [])
            for rec in recommendations:
                ai_suggestions.append(AIRecommendation(
                    brand_name=rec.get("brand_name", "AI 추천 브랜드"),
                    category=rec.get("target_audience", search_request.category or "일반"),
                    reason=rec.get("concept", "AI 기반 추천"),
                    confidence_score=0.8
                ))

    # Default suggestion if GPT fails
    if not ai_suggestions:
        ai_suggestions = [
            AIRecommendation(
                brand_name=f"{search_request.query} 관련 브랜드" if search_request.query else "추천 브랜드",
                category=search_request.category or "일반",
                reason="검색어 기반 추천",
                confidence_score=0.6
            )
        ]

    return BrandSearchResponse(
        brands=shortcuts,
        ai_suggestions=ai_suggestions,
        total_count=total_count or 0
    )
