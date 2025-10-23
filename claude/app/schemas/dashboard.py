"""
Dashboard Pydantic Schemas
Request and response models for dashboard endpoints
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class BrandShortcut(BaseModel):
    """Schema for brand shortcut card"""
    id: int
    brand_name: str
    category: Optional[str] = None
    logo_url: Optional[str] = None
    latest_kpi: Optional[float] = None
    kpi_trend: Optional[str] = Field(None, pattern="^(up|down|stable)$")  # up, down, stable
    updated_at: datetime

    class Config:
        from_attributes = True


class UserStatus(BaseModel):
    """Schema for user status and subscription"""
    subscription_status: str
    is_verified: bool
    total_brands: int
    total_campaigns: int
    last_login: Optional[datetime] = None


class AIRecommendation(BaseModel):
    """Schema for AI brand recommendation"""
    brand_name: str
    category: str
    reason: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)


class DashboardResponse(BaseModel):
    """Schema for main dashboard response"""
    welcome_message: str
    brand_shortcuts: List[BrandShortcut]
    user_status: UserStatus
    ai_recommendations: Optional[List[AIRecommendation]] = None
    recent_activity: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True


class BrandSearchRequest(BaseModel):
    """Schema for brand search request"""
    query: str = Field(..., min_length=1, max_length=200)
    category: Optional[str] = None
    limit: int = Field(10, ge=1, le=50)


class BrandSearchResponse(BaseModel):
    """Schema for brand search response"""
    brands: List[BrandShortcut]
    ai_suggestions: Optional[List[AIRecommendation]] = None
    total_count: int
