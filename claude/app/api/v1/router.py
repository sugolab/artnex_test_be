"""
API v1 Router
Combines all v1 endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import dashboard, auth, insights, design

api_router = APIRouter()

# Back1: Authentication & Dashboard
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)

# Back2: Brand Insights
api_router.include_router(
    insights.router,
    tags=["Brand Insights"]
)

# Back3: Design Studio
api_router.include_router(
    design.router,
    tags=["Design Studio"]
)

# Back3: Campaigns (추후 추가 예정)
# api_router.include_router(campaigns.router, tags=["Campaigns"])
