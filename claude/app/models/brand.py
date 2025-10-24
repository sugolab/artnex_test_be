"""
Brand and Brand KPI Models
Core brand management tables
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Brand(Base):
    """
    Brands table - Core brand information
    ERD Reference: Brands table
    """
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    brand_name = Column(String(200), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    industry = Column(String(100), nullable=True)
    slogan = Column(Text, nullable=True)
    mission = Column(Text, nullable=True)
    vision = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=True)  # Array of keywords
    logo_url = Column(String(500), nullable=True)
    website = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)

    # Brand identity
    tone_manner = Column(JSON, nullable=True)  # Tone and manner settings
    color_palette = Column(JSON, nullable=True)  # Brand colors

    # Metadata
    status = Column(String(50), default="active", nullable=False)  # active, inactive, archived
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="brands")
    kpis = relationship("BrandKPI", back_populates="brand", cascade="all, delete-orphan")

    # Back2 relationships
    insights = relationship("BrandInsight", back_populates="brand", cascade="all, delete-orphan")
    reports = relationship("BrandReport", back_populates="brand", cascade="all, delete-orphan")

    # Back3 relationships
    design_projects = relationship("DesignProject", back_populates="brand", cascade="all, delete-orphan")
    shortform_projects = relationship("ShortformProject", back_populates="brand", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="brand", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Brand(id={self.id}, brand_name='{self.brand_name}', category='{self.category}')>"


class BrandKPI(Base):
    """
    Brand KPIs table - Key Performance Indicators
    ERD Reference: Brand_KPIs table
    """
    __tablename__ = "brand_kpis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False, index=True)

    # KPI metrics
    kpi_type = Column(String(100), nullable=False, index=True)  # followers, engagement_rate, popularity_index, etc.
    value = Column(Float, nullable=False)
    measurement_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Social media metrics
    followers = Column(Integer, nullable=True)
    engagement_rate = Column(Float, nullable=True)
    avg_views = Column(Integer, nullable=True)
    avg_likes = Column(Integer, nullable=True)
    avg_comments = Column(Integer, nullable=True)

    # Calculated metrics
    popularity_index = Column(Float, nullable=True)  # Calculated using scipy

    # Metadata
    source = Column(String(100), nullable=True)  # youtube, tiktok, instagram, manual
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    brand = relationship("Brand", back_populates="kpis")

    def __repr__(self) -> str:
        return f"<BrandKPI(id={self.id}, brand_id={self.brand_id}, kpi_type='{self.kpi_type}', value={self.value})>"
