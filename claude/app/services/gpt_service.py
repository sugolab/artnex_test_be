"""
GPT Service
OpenAI API integration for AI-powered brand recommendations and analysis
"""
import os
import json
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from app.core.config import settings


class GPTService:
    """
    GPT Service for AI-powered features

    Features:
    - Brand recommendations based on user preferences
    - Market analysis and insights
    - Keyword generation and clustering
    - Brand positioning suggestions
    """

    def __init__(self):
        """Initialize GPT service with API key"""
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4-turbo-preview"
        self.temperature = 0.7
        self.max_tokens = 2000

    async def recommend_brands(
        self,
        industry: str,
        target_audience: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        limit: int = 5
    ) -> Dict:
        """
        Generate AI-powered brand recommendations

        Args:
            industry: Industry type (e.g., "뷰티", "식품", "패션")
            target_audience: Target audience description (e.g., "20대 여성")
            keywords: Related keywords
            limit: Number of recommendations to generate

        Returns:
            Dictionary containing brand recommendations and insights
        """
        # Build prompt
        prompt_parts = [f"{industry} 산업에서"]

        if target_audience:
            prompt_parts.append(f"{target_audience}를 타깃으로 하는")

        if keywords:
            keywords_str = ", ".join(keywords)
            prompt_parts.append(f"'{keywords_str}' 키워드와 관련된")

        prompt_parts.append(f"브랜드 아이디어를 {limit}개 추천해주세요.")

        prompt = " ".join(prompt_parts)

        system_prompt = """당신은 제조업 브랜드 마케팅 전문가입니다.
브랜드 아이디어를 제안할 때 다음 정보를 포함해주세요:
1. 브랜드명 아이디어
2. 핵심 컨셉
3. 타깃 고객
4. 차별화 포인트
5. 핵심 키워드

JSON 형식으로 응답해주세요:
{
    "recommendations": [
        {
            "brand_name": "브랜드명",
            "concept": "핵심 컨셉",
            "target_audience": "타깃 고객",
            "differentiation": "차별화 포인트",
            "keywords": ["키워드1", "키워드2", "키워드3"]
        }
    ],
    "market_insight": "시장 트렌드 및 인사이트"
}
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            result = json.loads(content)

            return {
                "success": True,
                "data": result,
                "tokens_used": response.usage.total_tokens
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    async def analyze_brand_positioning(
        self,
        brand_name: str,
        industry: str,
        mission: Optional[str] = None,
        target_audience: Optional[str] = None
    ) -> Dict:
        """
        Analyze brand positioning and provide strategic recommendations

        Args:
            brand_name: Brand name
            industry: Industry type
            mission: Brand mission statement
            target_audience: Target audience description

        Returns:
            Brand positioning analysis and recommendations
        """
        prompt_parts = [f"'{brand_name}' 브랜드의 포지셔닝을 분석해주세요."]
        prompt_parts.append(f"산업: {industry}")

        if mission:
            prompt_parts.append(f"미션: {mission}")

        if target_audience:
            prompt_parts.append(f"타깃 고객: {target_audience}")

        prompt = "\n".join(prompt_parts)

        system_prompt = """당신은 브랜드 전략 컨설턴트입니다.
브랜드 포지셔닝 분석 시 다음 내용을 포함해주세요:
1. 시장 내 위치
2. 경쟁 우위 요소
3. 타깃 고객 적합성
4. 개선 제안 사항
5. 추천 마케팅 전략

JSON 형식으로 응답해주세요:
{
    "positioning": {
        "market_position": "시장 내 위치 분석",
        "competitive_advantage": "경쟁 우위 요소",
        "target_fit": "타깃 고객 적합성 평가",
        "score": 75  // 0-100점
    },
    "recommendations": [
        {
            "category": "카테고리",
            "suggestion": "구체적인 제안",
            "priority": "high|medium|low"
        }
    ],
    "marketing_strategies": ["전략1", "전략2", "전략3"]
}
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            result = json.loads(content)

            return {
                "success": True,
                "data": result,
                "tokens_used": response.usage.total_tokens
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    async def generate_keywords(
        self,
        brand_name: str,
        industry: str,
        description: Optional[str] = None,
        limit: int = 20
    ) -> Dict:
        """
        Generate relevant keywords for brand

        Args:
            brand_name: Brand name
            industry: Industry type
            description: Brand description
            limit: Number of keywords to generate

        Returns:
            List of relevant keywords with categories
        """
        prompt = f"'{brand_name}' 브랜드를 위한 마케팅 키워드를 {limit}개 생성해주세요.\n"
        prompt += f"산업: {industry}\n"

        if description:
            prompt += f"설명: {description}\n"

        system_prompt = """당신은 SEO 및 마케팅 키워드 전문가입니다.
키워드는 다음 카테고리로 분류해주세요:
1. 제품 관련 (product)
2. 타깃 고객 (target)
3. 가치 제안 (value)
4. 감성적 (emotional)
5. 트렌드 (trend)

JSON 형식으로 응답해주세요:
{
    "keywords": [
        {
            "keyword": "키워드",
            "category": "product|target|value|emotional|trend",
            "relevance": 95  // 0-100점
        }
    ],
    "keyword_clusters": {
        "product": ["키워드1", "키워드2"],
        "target": ["키워드3", "키워드4"],
        "value": ["키워드5", "키워드6"],
        "emotional": ["키워드7", "키워드8"],
        "trend": ["키워드9", "키워드10"]
    }
}
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            result = json.loads(content)

            return {
                "success": True,
                "data": result,
                "tokens_used": response.usage.total_tokens
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }

    async def generate_improvement_suggestions(
        self,
        brand_data: Dict
    ) -> Dict:
        """
        Generate AI-powered improvement suggestions for brand

        Args:
            brand_data: Dictionary containing brand information
                - brand_name: str
                - category: str
                - current_kpis: dict (optional)
                - challenges: list (optional)

        Returns:
            Improvement suggestions and action items
        """
        brand_name = brand_data.get("brand_name", "")
        category = brand_data.get("category", "")
        current_kpis = brand_data.get("current_kpis", {})
        challenges = brand_data.get("challenges", [])

        prompt = f"'{brand_name}' 브랜드 ({category})의 개선 방안을 제안해주세요.\n"

        if current_kpis:
            prompt += f"\n현재 KPI:\n"
            for key, value in current_kpis.items():
                prompt += f"- {key}: {value}\n"

        if challenges:
            prompt += f"\n주요 도전과제:\n"
            for challenge in challenges:
                prompt += f"- {challenge}\n"

        system_prompt = """당신은 브랜드 개선 컨설턴트입니다.
브랜드 개선 방안을 제안할 때 다음 구조로 작성해주세요:
1. 현황 분석
2. 개선 영역 (브랜딩, 마케팅, 제품, 고객경험)
3. 구체적인 액션 아이템 (우선순위 포함)
4. 예상 효과

JSON 형식으로 응답해주세요:
{
    "analysis": "현황 분석 요약",
    "improvement_areas": [
        {
            "area": "브랜딩|마케팅|제품|고객경험",
            "current_status": "현재 상태",
            "target_status": "목표 상태",
            "gap_analysis": "격차 분석"
        }
    ],
    "action_items": [
        {
            "title": "액션 아이템 제목",
            "description": "상세 설명",
            "priority": "high|medium|low",
            "timeline": "1-3개월|3-6개월|6-12개월",
            "expected_impact": "예상 효과"
        }
    ],
    "overall_recommendations": "종합 추천사항"
}
"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            result = json.loads(content)

            return {
                "success": True,
                "data": result,
                "tokens_used": response.usage.total_tokens
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }


# Singleton instance
gpt_service = GPTService()
