"""
KPI Service
Brand KPI calculation and trend analysis
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.models.brand import BrandKPI


class KPIService:
    """
    KPI Service for calculating brand performance metrics and trends

    Features:
    - KPI trend calculation (up/down/stable)
    - Popularity index calculation
    - Performance comparison
    - Historical analysis
    """

    @staticmethod
    def calculate_popularity_index(
        followers: int,
        engagement_rate: float,
        avg_views: int,
        avg_likes: int,
        avg_comments: int
    ) -> float:
        """
        Calculate brand popularity index based on multiple metrics

        Formula:
        Popularity Index = (
            (followers * 0.3) +
            (engagement_rate * 100 * 0.25) +
            (avg_views * 0.2) +
            (avg_likes * 0.15) +
            (avg_comments * 0.10)
        ) / 1000

        Args:
            followers: Number of followers
            engagement_rate: Engagement rate (0-1)
            avg_views: Average views per post
            avg_likes: Average likes per post
            avg_comments: Average comments per post

        Returns:
            Popularity index score (0-100)
        """
        # Normalize metrics
        follower_score = (followers or 0) * 0.3
        engagement_score = (engagement_rate or 0) * 100 * 0.25
        views_score = (avg_views or 0) * 0.2
        likes_score = (avg_likes or 0) * 0.15
        comments_score = (avg_comments or 0) * 0.10

        # Calculate total score
        total_score = (
            follower_score +
            engagement_score +
            views_score +
            likes_score +
            comments_score
        ) / 1000

        # Cap at 100
        return min(total_score, 100.0)

    @staticmethod
    async def get_kpi_trend(
        db: AsyncSession,
        brand_id: int,
        kpi_type: str = "popularity_index",
        days: int = 30
    ) -> Literal["up", "down", "stable"]:
        """
        Calculate KPI trend for a brand over specified period

        Args:
            db: Database session
            brand_id: Brand ID
            kpi_type: Type of KPI to analyze (default: "popularity_index")
            days: Number of days to analyze (default: 30)

        Returns:
            Trend direction: "up", "down", or "stable"
        """
        # Get KPIs from the last N days
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        query = select(BrandKPI).where(
            BrandKPI.brand_id == brand_id,
            BrandKPI.measurement_date >= cutoff_date
        ).order_by(BrandKPI.measurement_date)

        result = await db.execute(query)
        kpis = result.scalars().all()

        if len(kpis) < 2:
            return "stable"  # Not enough data for trend analysis

        # Extract values based on kpi_type
        if kpi_type == "popularity_index":
            values = [kpi.popularity_index for kpi in kpis if kpi.popularity_index is not None]
        elif kpi_type == "followers":
            values = [kpi.followers for kpi in kpis if kpi.followers is not None]
        elif kpi_type == "engagement_rate":
            values = [kpi.engagement_rate for kpi in kpis if kpi.engagement_rate is not None]
        else:
            values = [kpi.value for kpi in kpis]

        if not values or len(values) < 2:
            return "stable"

        # Calculate trend using simple linear regression approach
        # Compare first half average vs second half average
        mid_point = len(values) // 2
        first_half_avg = sum(values[:mid_point]) / mid_point if mid_point > 0 else 0
        second_half_avg = sum(values[mid_point:]) / (len(values) - mid_point)

        # Calculate percentage change
        if first_half_avg == 0:
            return "up" if second_half_avg > 0 else "stable"

        percent_change = ((second_half_avg - first_half_avg) / first_half_avg) * 100

        # Determine trend based on percentage change threshold
        if percent_change > 5:  # More than 5% increase
            return "up"
        elif percent_change < -5:  # More than 5% decrease
            return "down"
        else:
            return "stable"

    @staticmethod
    async def get_kpi_summary(
        db: AsyncSession,
        brand_id: int
    ) -> Dict:
        """
        Get comprehensive KPI summary for a brand

        Args:
            db: Database session
            brand_id: Brand ID

        Returns:
            Dictionary containing current KPIs, trends, and statistics
        """
        # Get latest KPI
        latest_kpi_query = select(BrandKPI).where(
            BrandKPI.brand_id == brand_id
        ).order_by(desc(BrandKPI.measurement_date)).limit(1)

        latest_result = await db.execute(latest_kpi_query)
        latest_kpi = latest_result.scalar_one_or_none()

        if not latest_kpi:
            return {
                "current": None,
                "trends": {
                    "popularity_index": "stable",
                    "followers": "stable",
                    "engagement_rate": "stable"
                },
                "statistics": None
            }

        # Calculate trends for different metrics
        trends = {
            "popularity_index": await KPIService.get_kpi_trend(db, brand_id, "popularity_index", 30),
            "followers": await KPIService.get_kpi_trend(db, brand_id, "followers", 30),
            "engagement_rate": await KPIService.get_kpi_trend(db, brand_id, "engagement_rate", 30)
        }

        # Get historical statistics (last 90 days)
        stats_cutoff = datetime.utcnow() - timedelta(days=90)
        stats_query = select(
            func.avg(BrandKPI.popularity_index).label("avg_popularity"),
            func.max(BrandKPI.popularity_index).label("max_popularity"),
            func.min(BrandKPI.popularity_index).label("min_popularity"),
            func.avg(BrandKPI.followers).label("avg_followers"),
            func.avg(BrandKPI.engagement_rate).label("avg_engagement")
        ).where(
            BrandKPI.brand_id == brand_id,
            BrandKPI.measurement_date >= stats_cutoff
        )

        stats_result = await db.execute(stats_query)
        stats = stats_result.first()

        return {
            "current": {
                "popularity_index": latest_kpi.popularity_index,
                "followers": latest_kpi.followers,
                "engagement_rate": latest_kpi.engagement_rate,
                "avg_views": latest_kpi.avg_views,
                "avg_likes": latest_kpi.avg_likes,
                "avg_comments": latest_kpi.avg_comments,
                "measurement_date": latest_kpi.measurement_date
            },
            "trends": trends,
            "statistics": {
                "avg_popularity": float(stats.avg_popularity) if stats.avg_popularity else 0,
                "max_popularity": float(stats.max_popularity) if stats.max_popularity else 0,
                "min_popularity": float(stats.min_popularity) if stats.min_popularity else 0,
                "avg_followers": int(stats.avg_followers) if stats.avg_followers else 0,
                "avg_engagement": float(stats.avg_engagement) if stats.avg_engagement else 0
            } if stats else None
        }

    @staticmethod
    async def update_kpi(
        db: AsyncSession,
        brand_id: int,
        followers: Optional[int] = None,
        engagement_rate: Optional[float] = None,
        avg_views: Optional[int] = None,
        avg_likes: Optional[int] = None,
        avg_comments: Optional[int] = None,
        source: Optional[str] = "manual",
        notes: Optional[str] = None
    ) -> BrandKPI:
        """
        Update or create new KPI record for a brand

        Args:
            db: Database session
            brand_id: Brand ID
            followers: Number of followers
            engagement_rate: Engagement rate (0-1)
            avg_views: Average views per post
            avg_likes: Average likes per post
            avg_comments: Average comments per post
            source: Data source (manual, youtube, tiktok, instagram)
            notes: Additional notes

        Returns:
            Created BrandKPI object
        """
        # Calculate popularity index
        popularity_index = KPIService.calculate_popularity_index(
            followers=followers or 0,
            engagement_rate=engagement_rate or 0,
            avg_views=avg_views or 0,
            avg_likes=avg_likes or 0,
            avg_comments=avg_comments or 0
        )

        # Create new KPI record
        new_kpi = BrandKPI(
            brand_id=brand_id,
            kpi_type="social_media",
            value=popularity_index,
            measurement_date=datetime.utcnow(),
            followers=followers,
            engagement_rate=engagement_rate,
            avg_views=avg_views,
            avg_likes=avg_likes,
            avg_comments=avg_comments,
            popularity_index=popularity_index,
            source=source,
            notes=notes
        )

        db.add(new_kpi)
        await db.commit()
        await db.refresh(new_kpi)

        return new_kpi

    @staticmethod
    async def compare_brands(
        db: AsyncSession,
        brand_ids: List[int]
    ) -> List[Dict]:
        """
        Compare KPIs across multiple brands

        Args:
            db: Database session
            brand_ids: List of brand IDs to compare

        Returns:
            List of brand KPI comparisons
        """
        comparisons = []

        for brand_id in brand_ids:
            summary = await KPIService.get_kpi_summary(db, brand_id)
            comparisons.append({
                "brand_id": brand_id,
                "summary": summary
            })

        return comparisons


# Singleton instance
kpi_service = KPIService()
