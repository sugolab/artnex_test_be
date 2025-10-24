"""
Design Studio & Shortform Models (Back3)
디자인 스튜디오 및 숏폼 스튜디오 관련 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class DesignInputType(str, enum.Enum):
    """디자인 입력 유형"""
    IMPORT = "import"
    SCRIPT = "script"
    BLANK = "blank"


class DesignProject(Base):
    """디자인 프로젝트 테이블"""
    __tablename__ = "design_projects"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 프로젝트 정보
    project_name = Column(String(200), nullable=False)
    input_type = Column(Enum(DesignInputType), nullable=False)

    # 디자인 입력 데이터
    tone_manner = Column(JSON, comment="톤앤매너 차트 데이터")
    color_palette = Column(JSON, comment="컬러 팔레트")
    prompt = Column(Text, comment="디자인 프롬프트")
    keywords = Column(JSON, comment="디자인 키워드")

    # BID 연동
    bid_report_id = Column(Integer, ForeignKey("brand_reports.id", ondelete="SET NULL"), nullable=True)

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    brand = relationship("Brand", back_populates="design_projects")
    user = relationship("User", back_populates="design_projects")
    results = relationship("DesignResult", back_populates="project", cascade="all, delete-orphan")


class DesignResult(Base):
    """디자인 결과 테이블"""
    __tablename__ = "design_results"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("design_projects.id", ondelete="CASCADE"), nullable=False)

    # 이미지 정보
    image_url = Column(String(500), nullable=False, comment="생성된 이미지 URL")
    ideogram_id = Column(String(200), comment="Ideogram API 이미지 ID")

    # 생성 정보
    generation_prompt = Column(Text, comment="실제 사용된 프롬프트")
    style = Column(String(100), comment="스타일")
    industry_category = Column(String(100), comment="산업 카테고리")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    project = relationship("DesignProject", back_populates="results")
    mockups = relationship("DesignMockup", back_populates="design", cascade="all, delete-orphan")


class DesignMockup(Base):
    """디자인 목업 테이블"""
    __tablename__ = "design_mockups"

    id = Column(Integer, primary_key=True, index=True)
    design_result_id = Column(Integer, ForeignKey("design_results.id", ondelete="CASCADE"), nullable=False)

    # 목업 정보
    mockup_type = Column(String(100), comment="목업 유형 (패키지/명함/포스터 등)")
    mockup_url = Column(String(500), comment="목업 이미지 URL")
    industry_tab = Column(String(100), comment="산업별 탭")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    design = relationship("DesignResult", back_populates="mockups")


class ShortformProject(Base):
    """숏폼 프로젝트 테이블"""
    __tablename__ = "shortform_projects"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 프로젝트 정보
    project_name = Column(String(200), nullable=False)
    input_type = Column(Enum(DesignInputType), nullable=False)

    # 스크립트 정보
    script_text = Column(Text, comment="스크립트 텍스트")
    script_file_url = Column(String(500), comment="업로드된 스크립트 파일 URL")

    # 설정
    num_cuts = Column(Integer, comment="컷 수")
    aspect_ratio = Column(String(20), default="9:16", comment="영상 비율")
    language = Column(String(10), default="ko", comment="언어")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    brand = relationship("Brand", back_populates="shortform_projects")
    user = relationship("User", back_populates="shortform_projects")
    frames = relationship("StoryboardFrame", back_populates="project", cascade="all, delete-orphan")


class StoryboardFrame(Base):
    """스토리보드 프레임 테이블"""
    __tablename__ = "storyboard_frames"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("shortform_projects.id", ondelete="CASCADE"), nullable=False)

    # 프레임 정보
    frame_number = Column(Integer, nullable=False, comment="프레임 번호")
    dialogue = Column(Text, comment="대사/텍스트")
    shooting_note = Column(Text, comment="촬영 노트")

    # 이미지
    image_url = Column(String(500), comment="생성된 이미지 URL")
    image_prompt = Column(Text, comment="이미지 생성 프롬프트")

    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("ShortformProject", back_populates="frames")
