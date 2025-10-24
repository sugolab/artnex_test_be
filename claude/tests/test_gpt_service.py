"""
GPT Service Tests
GPT Service 단위 테스트
"""
import pytest
from app.services.gpt_service import GPTService


@pytest.mark.asyncio
async def test_recommend_brands():
    """브랜드 추천 테스트"""
    service = GPTService()

    result = await service.recommend_brands(
        industry="뷰티",
        target_audience="20대 여성",
        keywords=["비건", "친환경"],
        limit=3
    )

    assert isinstance(result, dict)
    assert "recommendations" in result or "success" in result


@pytest.mark.asyncio
async def test_analyze_brand_positioning():
    """브랜드 포지셔닝 분석 테스트"""
    service = GPTService()

    result = await service.analyze_brand_positioning(
        brand_name="Test Brand",
        industry="뷰티",
        competitors=["경쟁사A", "경쟁사B"]
    )

    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_generate_keywords():
    """키워드 생성 테스트"""
    service = GPTService()

    keywords = await service.generate_keywords(
        prompt="비건 화장품 브랜드",
        num_keywords=10
    )

    assert isinstance(keywords, list)
    assert len(keywords) <= 10


@pytest.mark.asyncio
async def test_analyze_market():
    """시장 분석 테스트 (Back2)"""
    service = GPTService()

    result = await service.analyze_market(
        prompt="20대 여성을 위한 비건 스킨케어 시장 분석",
        brand_id=1
    )

    assert isinstance(result, dict)
    assert "summary" in result
    assert "keywords" in result
    assert "market_data" in result
