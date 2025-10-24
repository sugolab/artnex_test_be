"""
Campaign Models (Back3)
캠페인 관리 및 캠페인 리포트 관련 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, Enum, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class CampaignStatus(str, enum.Enum):
    """캠페인 상태"""
    DRAFT = "draft"  # 초안
    ACTIVE = "active"  # 진행중
    PAUSED = "paused"  # 일시정지
    COMPLETED = "completed"  # 완료
    CANCELLED = "cancelled"  # 취소


class CampaignType(str, enum.Enum):
    """캠페인 유형"""
    SNS = "sns"  # SNS 광고
    INFLUENCER = "influencer"  # 인플루언서 마케팅
    EMAIL = "email"  # 이메일 마케팅
    CONTENT = "content"  # 콘텐츠 마케팅
    MIXED = "mixed"  # 복합


class Campaign(Base):
    """캠페인 테이블"""
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 캠페인 기본 정보
    campaign_name = Column(String(200), nullable=False)
    campaign_type = Column(Enum(CampaignType), nullable=False)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT, nullable=False)

    # 목표 및 예산
    goal = Column(Text, comment="캠페인 목표")
    budget = Column(Numeric(15, 2), comment="예산")
    budget_currency = Column(String(10), default="KRW", comment="통화")

    # 기간
    start_date = Column(DateTime(timezone=True), comment="시작일")
    end_date = Column(DateTime(timezone=True), comment="종료일")

    # 타겟
    target_audience = Column(JSON, comment="타겟 오디언스")
    target_keywords = Column(JSON, comment="타겟 키워드")

    # AI 추천
    ai_budget_recommendation = Column(JSON, comment="AI 예산 추천")
    ai_influencer_recommendations = Column(JSON, comment="AI 인플루언서 추천")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    brand = relationship("Brand", back_populates="campaigns")
    user = relationship("User", back_populates="campaigns")
    tracking = relationship("CampaignTracking", back_populates="campaign", cascade="all, delete-orphan")
    reports = relationship("CampaignReport", back_populates="campaign", cascade="all, delete-orphan")


class CampaignTracking(Base):
    """캠페인 추적 데이터 테이블"""
    __tablename__ = "campaign_tracking"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)

    # 추적 날짜
    tracking_date = Column(DateTime(timezone=True), nullable=False)

    # 성과 지표
    impressions = Column(Integer, default=0, comment="노출수")
    clicks = Column(Integer, default=0, comment="클릭수")
    conversions = Column(Integer, default=0, comment="전환수")
    revenue = Column(Numeric(15, 2), default=0, comment="매출")
    cost = Column(Numeric(15, 2), default=0, comment="비용")

    # 계산 지표
    ctr = Column(Float, comment="CTR (Click-Through Rate)")
    cpc = Column(Numeric(10, 2), comment="CPC (Cost Per Click)")
    roas = Column(Float, comment="ROAS (Return on Ad Spend)")

    # 소셜 지표
    likes = Column(Integer, default=0, comment="좋아요")
    shares = Column(Integer, default=0, comment="공유")
    comments = Column(Integer, default=0, comment="댓글")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    campaign = relationship("Campaign", back_populates="tracking")


class CampaignReport(Base):
    """캠페인 리포트 테이블"""
    __tablename__ = "campaign_reports"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)

    # 리포트 기간
    report_month = Column(String(7), nullable=False, comment="리포트 월 (YYYY-MM)")
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)

    # KPI 요약
    total_revenue = Column(Numeric(15, 2), comment="총 매출")
    total_sales = Column(Integer, comment="총 판매량")
    total_products = Column(Integer, comment="총 상품수")
    total_cost = Column(Numeric(15, 2), comment="총 비용")

    # 성과 분석
    top_campaigns = Column(JSON, comment="상위 캠페인")
    top_customers = Column(JSON, comment="상위 고객")
    top_products = Column(JSON, comment="상위 제품")
    channel_performance = Column(JSON, comment="채널별 성과")

    # AI 분석
    ai_summary = Column(Text, comment="AI 요약")
    ai_predictions = Column(JSON, comment="AI 성과 예측")
    ai_recommendations = Column(JSON, comment="AI 개선 제안")

    # 소셜 퍼포먼스
    social_performance = Column(JSON, comment="SNS 유입 비율 및 성과")

    # Export 정보
    pdf_url = Column(String(500), comment="PDF URL")
    excel_url = Column(String(500), comment="Excel URL")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    campaign = relationship("Campaign", back_populates="reports")
