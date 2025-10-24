"""
ArtNex Database Models
SQLAlchemy ORM models for all tables
"""
# Back1 models
from app.models.user import User, Role
from app.models.brand import Brand, BrandKPI

# Back2 models (Brand Insight & Report)
from app.models.insight import (
    BrandInsight,
    InsightResult,
    BrandReport,
    BrandDiagnostic,
    ReportSection,
    InsightType,
    DiagnosticSection
)

# Back3 models (Design & Campaign)
from app.models.design import (
    DesignProject,
    DesignResult,
    DesignMockup,
    ShortformProject,
    StoryboardFrame,
    DesignInputType
)
from app.models.campaign import (
    Campaign,
    CampaignTracking,
    CampaignReport,
    CampaignStatus,
    CampaignType
)

__all__ = [
    # Back1
    "User",
    "Role",
    "Brand",
    "BrandKPI",
    # Back2
    "BrandInsight",
    "InsightResult",
    "BrandReport",
    "BrandDiagnostic",
    "ReportSection",
    "InsightType",
    "DiagnosticSection",
    # Back3
    "DesignProject",
    "DesignResult",
    "DesignMockup",
    "ShortformProject",
    "StoryboardFrame",
    "DesignInputType",
    "Campaign",
    "CampaignTracking",
    "CampaignReport",
    "CampaignStatus",
    "CampaignType",
]
