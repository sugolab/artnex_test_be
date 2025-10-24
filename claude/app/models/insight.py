"""
Brand Insight Models (Back2)
브랜드 인사이트 및 리포트 관련 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class InsightType(str, enum.Enum):
    """인사이트 유형"""
    MARKET_ANALYSIS = "market_analysis"
    KEYWORD_CLUSTERING = "keyword_clustering"
    INFLUENCER_RECOMMENDATION = "influencer_recommendation"
    VISUAL_PROPOSAL = "visual_proposal"
    ITEM_SUGGESTION = "item_suggestion"


class DiagnosticSection(str, enum.Enum):
    """진단 섹션"""
    MARKET = "market"  # 시장
    COMPETITOR = "competitor"  # 경쟁사
    MANUFACTURING = "manufacturing"  # 제조
    BRAND = "brand"  # 브랜드
    MARKETING = "marketing"  # 마케팅


class BrandInsight(Base):
    """브랜드 인사이트 테이블"""
    __tablename__ = "brand_insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="SET NULL"), nullable=True)

    # 프롬프트 및 결과
    prompt = Column(Text, nullable=False, comment="사용자 입력 프롬프트")
    insight_type = Column(Enum(InsightType), nullable=False)

    # AI 분석 결과
    analysis_summary = Column(Text, comment="AI 분석 요약")
    keywords = Column(JSON, comment="추출된 키워드 리스트")
    market_data = Column(JSON, comment="시장 데이터")
    recommendations = Column(JSON, comment="추천 사항")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="insights")
    brand = relationship("Brand", back_populates="insights")
    results = relationship("InsightResult", back_populates="insight", cascade="all, delete-orphan")


class InsightResult(Base):
    """인사이트 결과 상세 테이블"""
    __tablename__ = "insight_results"

    id = Column(Integer, primary_key=True, index=True)
    insight_id = Column(Integer, ForeignKey("brand_insights.id", ondelete="CASCADE"), nullable=False)

    # 결과 데이터
    title = Column(String(500), comment="결과 제목")
    description = Column(Text, comment="결과 설명")
    category = Column(String(100), comment="결과 카테고리")
    confidence_score = Column(Float, comment="신뢰도 점수 (0-100)")
    data = Column(JSON, comment="상세 데이터")
    image_url = Column(String(500), comment="이미지 URL")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    insight = relationship("BrandInsight", back_populates="results")


class BrandReport(Base):
    """브랜드 리포트 테이블"""
    __tablename__ = "brand_reports"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 리포트 정보
    report_name = Column(String(200), nullable=False)
    report_type = Column(String(50), default="diagnostic", comment="리포트 유형")

    # 전체 점수
    overall_score = Column(Float, comment="전체 점수 (0-100)")

    # AI 분석
    ai_summary = Column(Text, comment="AI 생성 요약")
    ai_recommendations = Column(JSON, comment="AI 개선 제안")

    # PDF 정보
    pdf_url = Column(String(500), comment="생성된 PDF URL")
    pdf_language = Column(String(10), default="ko", comment="리포트 언어 (ko/en)")
    pdf_color_scheme = Column(String(50), comment="컬러 스킴")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    brand = relationship("Brand", back_populates="reports")
    user = relationship("User", back_populates="reports")
    diagnostics = relationship("BrandDiagnostic", back_populates="report", cascade="all, delete-orphan")
    sections = relationship("ReportSection", back_populates="report", cascade="all, delete-orphan")


class BrandDiagnostic(Base):
    """브랜드 진단 데이터 테이블 (5단계 폼)"""
    __tablename__ = "brand_diagnostics"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("brand_reports.id", ondelete="CASCADE"), nullable=False)

    # 진단 섹션
    section = Column(Enum(DiagnosticSection), nullable=False)

    # 진단 데이터 (5점 척도)
    questions_answers = Column(JSON, nullable=False, comment="질문-응답 데이터")
    section_score = Column(Float, comment="섹션 점수 (0-100)")

    # AI 분석
    ai_analysis = Column(Text, comment="AI 분석 코멘트")
    strengths = Column(JSON, comment="강점")
    weaknesses = Column(JSON, comment="약점")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    report = relationship("BrandReport", back_populates="diagnostics")


class ReportSection(Base):
    """리포트 섹션 테이블"""
    __tablename__ = "report_sections"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("brand_reports.id", ondelete="CASCADE"), nullable=False)

    # 섹션 정보
    section_name = Column(String(100), nullable=False, comment="섹션명 (타겟/키워드/매니징/디자인/마케팅)")
    section_order = Column(Integer, default=0, comment="섹션 순서")

    # 섹션 데이터
    content = Column(JSON, comment="섹션 콘텐츠 데이터")
    chart_data = Column(JSON, comment="차트 데이터")
    insights = Column(JSON, comment="인사이트 데이터")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    report = relationship("BrandReport", back_populates="sections")
