"""
Campaign Pydantic Schemas (Back3)
Request/Response validation for Campaign APIs
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from app.models.campaign import CampaignStatus, CampaignType


# ========================================
# Campaign Schemas
# ========================================

class CampaignCreate(BaseModel):
    """캠페인 생성 요청"""
    brand_id: int
    campaign_name: str = Field(..., min_length=1, max_length=200)
    campaign_type: CampaignType
    goal: Optional[str] = None
    budget: Optional[Decimal] = Field(None, ge=0)
    budget_currency: str = Field(default="KRW", max_length=10)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    target_audience: Optional[Dict[str, Any]] = None
    target_keywords: Optional[List[str]] = None


class CampaignUpdate(BaseModel):
    """캠페인 업데이트"""
    campaign_name: Optional[str] = Field(None, max_length=200)
    status: Optional[CampaignStatus] = None
    goal: Optional[str] = None
    budget: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class CampaignResponse(BaseModel):
    """캠페인 응답"""
    id: int
    brand_id: int
    user_id: int
    campaign_name: str
    campaign_type: CampaignType
    status: CampaignStatus
    goal: Optional[str]
    budget: Optional[Decimal]
    budget_currency: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    target_audience: Optional[Dict[str, Any]]
    target_keywords: Optional[List[str]]
    ai_budget_recommendation: Optional[Dict[str, Any]]
    ai_influencer_recommendations: Optional[List[Dict[str, Any]]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CampaignListResponse(BaseModel):
    """캠페인 목록 응답"""
    total: int
    page: int
    page_size: int
    campaigns: List[CampaignResponse]


class CampaignSummary(BaseModel):
    """캠페인 요약"""
    total_campaigns: int
    active_campaigns: int
    total_budget: Decimal
    total_revenue: Optional[Decimal]


# ========================================
# Campaign Tracking Schemas
# ========================================

class CampaignTrackingCreate(BaseModel):
    """캠페인 추적 데이터 생성"""
    campaign_id: int
    tracking_date: datetime
    impressions: int = Field(default=0, ge=0)
    clicks: int = Field(default=0, ge=0)
    conversions: int = Field(default=0, ge=0)
    revenue: Decimal = Field(default=0, ge=0)
    cost: Decimal = Field(default=0, ge=0)


# ========================================
# Campaign Report Schemas
# ========================================

class CampaignReportCreate(BaseModel):
    """캠페인 리포트 생성"""
    campaign_id: int
    report_month: str = Field(..., pattern="^\\d{4}-\\d{2}$", description="YYYY-MM 형식")
    start_date: datetime
    end_date: datetime


class CampaignReportResponse(BaseModel):
    """캠페인 리포트 응답"""
    id: int
    campaign_id: int
    report_month: str
    start_date: datetime
    end_date: datetime
    total_revenue: Optional[Decimal]
    total_sales: Optional[int]
    total_products: Optional[int]
    total_cost: Optional[Decimal]
    top_campaigns: Optional[List[Dict[str, Any]]]
    top_customers: Optional[List[Dict[str, Any]]]
    top_products: Optional[List[Dict[str, Any]]]
    channel_performance: Optional[Dict[str, Any]]
    ai_summary: Optional[str]
    ai_predictions: Optional[Dict[str, Any]]
    ai_recommendations: Optional[List[Dict[str, Any]]]
    social_performance: Optional[Dict[str, Any]]
    pdf_url: Optional[str]
    excel_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
