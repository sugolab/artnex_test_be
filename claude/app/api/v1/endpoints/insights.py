"""
Brand Insight API Endpoints (Back2)
브랜드 인사이트 GPT 연동 API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.insight import BrandInsight, InsightResult, InsightType
from app.schemas.insight import (
    BrandInsightCreate,
    BrandInsightResponse,
    BrandInsightListResponse
)
from app.services.gpt_service import GPTService
import json

router = APIRouter()


@router.post("/insights", response_model=BrandInsightResponse, status_code=201)
async def create_brand_insight(
    insight_data: BrandInsightCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    브랜드 인사이트 생성 및 GPT 분석

    **Back2 Day 1 작업**: 프롬프트 입력 API 설계 및 GPT 시장조사 로직
    """
    gpt_service = GPTService()

    # GPT를 활용한 시장 분석
    if insight_data.insight_type == InsightType.MARKET_ANALYSIS:
        # 시장 분석 요청
        analysis = await gpt_service.analyze_market(
            prompt=insight_data.prompt,
            brand_id=insight_data.brand_id
        )

        # 인사이트 데이터 생성
        insight = BrandInsight(
            user_id=current_user.id,
            brand_id=insight_data.brand_id,
            prompt=insight_data.prompt,
            insight_type=insight_data.insight_type,
            analysis_summary=analysis.get("summary"),
            keywords=analysis.get("keywords", []),
            market_data=analysis.get("market_data"),
            recommendations=analysis.get("recommendations", [])
        )

        db.add(insight)
        await db.commit()
        await db.refresh(insight)

        # 인사이트 결과 생성
        if "items" in analysis:
            for idx, item in enumerate(analysis["items"][:5]):  # 최대 5개
                result = InsightResult(
                    insight_id=insight.id,
                    title=item.get("title", f"제안 {idx+1}"),
                    description=item.get("description"),
                    category=item.get("category", "general"),
                    confidence_score=item.get("confidence", 75.0),
                    data=item
                )
                db.add(result)

        await db.commit()
        await db.refresh(insight)

        return insight

    elif insight_data.insight_type == InsightType.KEYWORD_CLUSTERING:
        # 키워드 클러스터링 분석
        keywords = await gpt_service.generate_keywords(
            prompt=insight_data.prompt,
            num_keywords=20
        )

        insight = BrandInsight(
            user_id=current_user.id,
            brand_id=insight_data.brand_id,
            prompt=insight_data.prompt,
            insight_type=insight_data.insight_type,
            analysis_summary=f"{len(keywords)}개의 키워드 클러스터 생성",
            keywords=keywords,
            market_data={"total_keywords": len(keywords)}
        )

        db.add(insight)
        await db.commit()
        await db.refresh(insight)

        return insight

    else:
        # 기본 인사이트 생성
        insight = BrandInsight(
            user_id=current_user.id,
            brand_id=insight_data.brand_id,
            prompt=insight_data.prompt,
            insight_type=insight_data.insight_type
        )

        db.add(insight)
        await db.commit()
        await db.refresh(insight)

        return insight


@router.get("/insights", response_model=BrandInsightListResponse)
async def list_insights(
    brand_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    브랜드 인사이트 목록 조회
    """
    query = select(BrandInsight).where(BrandInsight.user_id == current_user.id)

    if brand_id:
        query = query.where(BrandInsight.brand_id == brand_id)

    query = query.order_by(BrandInsight.created_at.desc())

    # 페이지네이션
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    insights = result.scalars().all()

    # 전체 개수
    count_result = await db.execute(
        select(BrandInsight).where(BrandInsight.user_id == current_user.id)
    )
    total = len(count_result.scalars().all())

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "insights": insights
    }


@router.get("/insights/{insight_id}", response_model=BrandInsightResponse)
async def get_insight(
    insight_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    브랜드 인사이트 상세 조회
    """
    insight = await db.get(BrandInsight, insight_id)

    if not insight or insight.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="인사이트를 찾을 수 없습니다")

    return insight
