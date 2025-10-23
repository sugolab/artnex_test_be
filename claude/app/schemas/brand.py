"""
Brand Pydantic Schemas
Request and response models for brand-related endpoints
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class BrandBase(BaseModel):
    """Base brand schema"""
    brand_name: str = Field(..., min_length=1, max_length=200)
    category: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    slogan: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    keywords: Optional[List[str]] = None
    logo_url: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None


class BrandCreate(BrandBase):
    """Schema for creating a new brand"""
    tone_manner: Optional[Dict[str, Any]] = None
    color_palette: Optional[Dict[str, Any]] = None


class BrandUpdate(BaseModel):
    """Schema for updating a brand"""
    brand_name: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = Field(None, max_length=100)
    industry: Optional[str] = Field(None, max_length=100)
    slogan: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    keywords: Optional[List[str]] = None
    logo_url: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    tone_manner: Optional[Dict[str, Any]] = None
    color_palette: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, pattern="^(active|inactive|archived)$")


class BrandResponse(BrandBase):
    """Schema for brand response"""
    id: int
    user_id: int
    tone_manner: Optional[Dict[str, Any]] = None
    color_palette: Optional[Dict[str, Any]] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BrandKPIResponse(BaseModel):
    """Schema for brand KPI response"""
    id: int
    brand_id: int
    kpi_type: str
    value: float
    followers: Optional[int] = None
    engagement_rate: Optional[float] = None
    popularity_index: Optional[float] = None
    measurement_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
