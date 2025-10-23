"""
API v1 Router
Combines all v1 endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import dashboard

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)
