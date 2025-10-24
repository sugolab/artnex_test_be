"""
Brand Insight Pydantic Schemas (Back2)
Request/Response validation for Brand Insight APIs
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.insight import InsightType, DiagnosticSection


# ========================================
# Brand Insight Schemas
# ========================================

class InsightResultBase(BaseModel):
    """인사이트 결과 기본 스키마"""
    title: str = Field(..., max_length=500)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    confidence_score: Optional[float] = Field(None, ge=0, le=100)
    data: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = Field(None, max_length=500)


class InsightResultResponse(InsightResultBase):
    """인사이트 결과 응답"""
    id: int
    insight_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BrandInsightCreate(BaseModel):
    """브랜드 인사이트 생성 요청"""
    brand_id: Optional[int] = None
    prompt: str = Field(..., min_length=10, max_length=5000, description="분석 프롬프트")
    insight_type: InsightType = Field(default=InsightType.MARKET_ANALYSIS)

    @validator('prompt')
    def validate_prompt(cls, v):
        if not v.strip():
            raise ValueError('프롬프트는 공백일 수 없습니다')
        return v.strip()


class BrandInsightResponse(BaseModel):
    """브랜드 인사이트 응답"""
    id: int
    user_id: int
    brand_id: Optional[int]
    prompt: str
    insight_type: InsightType
    analysis_summary: Optional[str]
    keywords: Optional[List[str]]
    market_data: Optional[Dict[str, Any]]
    recommendations: Optional[List[Dict[str, Any]]]
    created_at: datetime
    updated_at: Optional[datetime]
    results: List[InsightResultResponse] = []

    class Config:
        from_attributes = True


class BrandInsightListResponse(BaseModel):
    """인사이트 목록 응답"""
    total: int
    page: int
    page_size: int
    insights: List[BrandInsightResponse]


# ========================================
# Brand Report Schemas
# ========================================

class BrandDiagnosticCreate(BaseModel):
    """브랜드 진단 생성 요청"""
    section: DiagnosticSection
    questions_answers: Dict[str, Any] = Field(..., description="질문-응답 데이터")

    @validator('questions_answers')
    def validate_qa(cls, v):
        if not v:
            raise ValueError('질문-응답 데이터는 필수입니다')
        return v


class BrandDiagnosticResponse(BaseModel):
    """브랜드 진단 응답"""
    id: int
    report_id: int
    section: DiagnosticSection
    questions_answers: Dict[str, Any]
    section_score: Optional[float]
    ai_analysis: Optional[str]
    strengths: Optional[List[str]]
    weaknesses: Optional[List[str]]
    created_at: datetime

    class Config:
        from_attributes = True


class ReportSectionCreate(BaseModel):
    """리포트 섹션 생성"""
    section_name: str = Field(..., max_length=100)
    section_order: int = Field(default=0, ge=0)
    content: Optional[Dict[str, Any]] = None
    chart_data: Optional[Dict[str, Any]] = None
    insights: Optional[List[Dict[str, Any]]] = None


class ReportSectionResponse(BaseModel):
    """리포트 섹션 응답"""
    id: int
    report_id: int
    section_name: str
    section_order: int
    content: Optional[Dict[str, Any]]
    chart_data: Optional[Dict[str, Any]]
    insights: Optional[List[Dict[str, Any]]]
    created_at: datetime

    class Config:
        from_attributes = True


class BrandReportCreate(BaseModel):
    """브랜드 리포트 생성 요청"""
    brand_id: int
    report_name: str = Field(..., min_length=1, max_length=200)
    report_type: str = Field(default="diagnostic", max_length=50)
    diagnostics: List[BrandDiagnosticCreate] = Field(default=[])


class BrandReportUpdate(BaseModel):
    """브랜드 리포트 업데이트"""
    report_name: Optional[str] = Field(None, max_length=200)
    overall_score: Optional[float] = Field(None, ge=0, le=100)
    ai_summary: Optional[str] = None
    ai_recommendations: Optional[List[Dict[str, Any]]] = None
    pdf_language: Optional[str] = Field(None, max_length=10)
    pdf_color_scheme: Optional[str] = Field(None, max_length=50)


class BrandReportResponse(BaseModel):
    """브랜드 리포트 응답"""
    id: int
    brand_id: int
    user_id: int
    report_name: str
    report_type: str
    overall_score: Optional[float]
    ai_summary: Optional[str]
    ai_recommendations: Optional[List[Dict[str, Any]]]
    pdf_url: Optional[str]
    pdf_language: str
    pdf_color_scheme: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    diagnostics: List[BrandDiagnosticResponse] = []
    sections: List[ReportSectionResponse] = []

    class Config:
        from_attributes = True


class BrandReportListResponse(BaseModel):
    """리포트 목록 응답"""
    total: int
    page: int
    page_size: int
    reports: List[BrandReportResponse]


class ReportExportRequest(BaseModel):
    """리포트 Export 요청"""
    language: str = Field(default="ko", pattern="^(ko|en)$")
    color_scheme: Optional[str] = Field(None, max_length=50)
    include_charts: bool = Field(default=True)
    include_ai_summary: bool = Field(default=True)


class ReportExportResponse(BaseModel):
    """리포트 Export 응답"""
    success: bool
    pdf_url: str
    file_size: Optional[int]
    generated_at: datetime
