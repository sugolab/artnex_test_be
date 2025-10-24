"""Pydantic Schemas"""
# Back1 schemas
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from app.schemas.brand import BrandCreate, BrandResponse, BrandUpdate
from app.schemas.dashboard import DashboardResponse, BrandShortcut, UserStatus

# Back2 schemas (Brand Insight & Report)
from app.schemas.insight import (
    BrandInsightCreate, BrandInsightResponse, BrandInsightListResponse,
    BrandReportCreate, BrandReportResponse, BrandReportUpdate,
    BrandDiagnosticCreate, ReportExportRequest, ReportExportResponse
)

# Back3 schemas (Design & Campaign)
from app.schemas.design import (
    DesignProjectCreate, DesignProjectResponse, DesignProjectUpdate,
    ShortformProjectCreate, ShortformProjectResponse, IdeogramGenerateRequest
)
from app.schemas.campaign import (
    CampaignCreate, CampaignResponse, CampaignUpdate, CampaignListResponse,
    CampaignReportCreate, CampaignReportResponse, CampaignSummary
)

__all__ = [
    # Back1
    "UserCreate", "UserResponse", "UserLogin", "TokenResponse",
    "BrandCreate", "BrandResponse", "BrandUpdate",
    "DashboardResponse", "BrandShortcut", "UserStatus",
    # Back2
    "BrandInsightCreate", "BrandInsightResponse", "BrandInsightListResponse",
    "BrandReportCreate", "BrandReportResponse", "BrandReportUpdate",
    "BrandDiagnosticCreate", "ReportExportRequest", "ReportExportResponse",
    # Back3
    "DesignProjectCreate", "DesignProjectResponse", "DesignProjectUpdate",
    "ShortformProjectCreate", "ShortformProjectResponse", "IdeogramGenerateRequest",
    "CampaignCreate", "CampaignResponse", "CampaignUpdate", "CampaignListResponse",
    "CampaignReportCreate", "CampaignReportResponse", "CampaignSummary",
]
