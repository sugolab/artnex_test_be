"""
Design Studio Pydantic Schemas (Back3)
Request/Response validation for Design Studio APIs
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.design import DesignInputType


# ========================================
# Design Project Schemas
# ========================================

class DesignProjectCreate(BaseModel):
    """디자인 프로젝트 생성 요청"""
    brand_id: int
    project_name: str = Field(..., min_length=1, max_length=200)
    input_type: DesignInputType
    tone_manner: Optional[Dict[str, Any]] = None
    color_palette: Optional[List[str]] = None
    prompt: Optional[str] = Field(None, max_length=2000)
    keywords: Optional[List[str]] = None
    bid_report_id: Optional[int] = None


class DesignProjectUpdate(BaseModel):
    """디자인 프로젝트 업데이트"""
    project_name: Optional[str] = Field(None, max_length=200)
    tone_manner: Optional[Dict[str, Any]] = None
    color_palette: Optional[List[str]] = None
    prompt: Optional[str] = Field(None, max_length=2000)


class DesignResultResponse(BaseModel):
    """디자인 결과 응답"""
    id: int
    project_id: int
    image_url: str
    ideogram_id: Optional[str]
    generation_prompt: Optional[str]
    style: Optional[str]
    industry_category: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DesignProjectResponse(BaseModel):
    """디자인 프로젝트 응답"""
    id: int
    brand_id: int
    user_id: int
    project_name: str
    input_type: DesignInputType
    tone_manner: Optional[Dict[str, Any]]
    color_palette: Optional[List[str]]
    prompt: Optional[str]
    keywords: Optional[List[str]]
    created_at: datetime
    updated_at: Optional[datetime]
    results: List[DesignResultResponse] = []

    class Config:
        from_attributes = True


class IdeogramGenerateRequest(BaseModel):
    """Ideogram 이미지 생성 요청"""
    project_id: int
    custom_prompt: Optional[str] = None
    style: Optional[str] = Field(None, max_length=100)


# ========================================
# Shortform Project Schemas
# ========================================

class ShortformProjectCreate(BaseModel):
    """숏폼 프로젝트 생성 요청"""
    brand_id: int
    project_name: str = Field(..., min_length=1, max_length=200)
    input_type: DesignInputType
    script_text: Optional[str] = Field(None, max_length=10000)
    num_cuts: Optional[int] = Field(None, ge=1, le=50)
    aspect_ratio: str = Field(default="9:16", pattern="^(9:16|16:9|1:1)$")
    language: str = Field(default="ko", max_length=10)


class StoryboardFrameResponse(BaseModel):
    """스토리보드 프레임 응답"""
    id: int
    project_id: int
    frame_number: int
    dialogue: Optional[str]
    shooting_note: Optional[str]
    image_url: Optional[str]
    image_prompt: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ShortformProjectResponse(BaseModel):
    """숏폼 프로젝트 응답"""
    id: int
    brand_id: int
    user_id: int
    project_name: str
    input_type: DesignInputType
    script_text: Optional[str]
    num_cuts: Optional[int]
    aspect_ratio: str
    language: str
    created_at: datetime
    updated_at: Optional[datetime]
    frames: List[StoryboardFrameResponse] = []

    class Config:
        from_attributes = True
