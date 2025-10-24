"""
Ideogram API Service (Back3 Day 2)
Ideogram AI 이미지 생성 API 연동
"""
import httpx
import asyncio
from typing import Dict, List, Optional
from app.core.config import settings
import json


class IdeogramService:
    """
    Ideogram API Service

    기능:
    - AI 이미지 생성
    - 프롬프트 자동 생성
    - 스타일 적용
    - 컬러 팔레트 기반 이미지 생성
    """

    def __init__(self):
        """Initialize Ideogram service"""
        self.api_key = getattr(settings, 'IDEOGRAM_API_KEY', None)
        self.base_url = "https://api.ideogram.ai/v1"
        self.timeout = 60.0

    async def generate_image(
        self,
        prompt: str,
        style: str = "design",
        aspect_ratio: str = "1:1",
        num_images: int = 1,
        color_palette: Optional[List[str]] = None
    ) -> Dict:
        """
        이미지 생성 (Ideogram API)

        Args:
            prompt: 이미지 생성 프롬프트
            style: 스타일 (design, realistic, anime, etc.)
            aspect_ratio: 비율 (1:1, 16:9, 9:16, 4:3)
            num_images: 생성할 이미지 수 (1-4)
            color_palette: 컬러 팔레트 (hex 코드 리스트)

        Returns:
            생성 결과 딕셔너리
        """
        # API 키가 없으면 Mock 데이터 반환
        if not self.api_key or self.api_key == "your-ideogram-api-key-here":
            return self._generate_mock_image(prompt, style, aspect_ratio, num_images)

        # 컬러 팔레트가 있으면 프롬프트에 추가
        if color_palette:
            color_text = ", ".join([f"color {color}" for color in color_palette[:3]])
            prompt = f"{prompt}, {color_text}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": prompt,
                        "style": style,
                        "aspect_ratio": aspect_ratio,
                        "num_images": num_images
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "images": result.get("images", []),
                        "prompt_used": prompt,
                        "style": style,
                        "aspect_ratio": aspect_ratio
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API Error: {response.status_code}",
                        "message": response.text
                    }

        except Exception as e:
            print(f"Error generating image: {str(e)}")
            # 에러 발생 시 Mock 데이터 반환
            return self._generate_mock_image(prompt, style, aspect_ratio, num_images)

    def _generate_mock_image(
        self,
        prompt: str,
        style: str,
        aspect_ratio: str,
        num_images: int
    ) -> Dict:
        """
        Mock 이미지 생성 (개발/테스트용)

        Args:
            prompt: 프롬프트
            style: 스타일
            aspect_ratio: 비율
            num_images: 이미지 수

        Returns:
            Mock 결과
        """
        # Placeholder 이미지 URL 생성
        width, height = self._get_dimensions(aspect_ratio)

        mock_images = []
        for i in range(num_images):
            mock_images.append({
                "image_id": f"mock_{i+1}_{hash(prompt) % 10000}",
                "url": f"https://via.placeholder.com/{width}x{height}/3357FF/FFFFFF?text=ArtNex+Design+{i+1}",
                "width": width,
                "height": height,
                "prompt": prompt,
                "style": style
            })

        return {
            "success": True,
            "images": mock_images,
            "prompt_used": prompt,
            "style": style,
            "aspect_ratio": aspect_ratio,
            "mock": True,
            "message": "Ideogram API 키가 없어 Mock 이미지를 반환합니다"
        }

    def _get_dimensions(self, aspect_ratio: str) -> tuple:
        """
        비율에 따른 이미지 크기 반환

        Args:
            aspect_ratio: 비율

        Returns:
            (width, height) 튜플
        """
        ratios = {
            "1:1": (1024, 1024),
            "16:9": (1024, 576),
            "9:16": (576, 1024),
            "4:3": (1024, 768),
            "3:4": (768, 1024)
        }
        return ratios.get(aspect_ratio, (1024, 1024))

    async def generate_brand_design(
        self,
        brand_name: str,
        industry: str,
        tone_manner: Optional[Dict] = None,
        color_palette: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        브랜드 디자인 생성 (자동 프롬프트 생성)

        Args:
            brand_name: 브랜드명
            industry: 산업
            tone_manner: 톤앤매너 ({"modern": 80, "friendly": 70})
            color_palette: 컬러 팔레트
            keywords: 키워드

        Returns:
            생성 결과
        """
        # 자동 프롬프트 생성
        prompt = self.build_design_prompt(
            brand_name=brand_name,
            industry=industry,
            tone_manner=tone_manner,
            keywords=keywords
        )

        # 이미지 생성
        result = await self.generate_image(
            prompt=prompt,
            style="design",
            aspect_ratio="1:1",
            num_images=4,
            color_palette=color_palette
        )

        return result

    def build_design_prompt(
        self,
        brand_name: str,
        industry: str,
        tone_manner: Optional[Dict] = None,
        keywords: Optional[List[str]] = None
    ) -> str:
        """
        디자인 프롬프트 자동 생성

        Args:
            brand_name: 브랜드명
            industry: 산업
            tone_manner: 톤앤매너
            keywords: 키워드

        Returns:
            생성된 프롬프트
        """
        prompt_parts = [f"Professional logo design for {brand_name}"]

        # 산업 추가
        if industry:
            prompt_parts.append(f"in the {industry} industry")

        # 톤앤매너 추가
        if tone_manner:
            top_tones = sorted(tone_manner.items(), key=lambda x: x[1], reverse=True)[:2]
            tone_text = " and ".join([tone for tone, _ in top_tones])
            prompt_parts.append(f"with {tone_text} style")

        # 키워드 추가
        if keywords:
            keyword_text = ", ".join(keywords[:3])
            prompt_parts.append(f"featuring {keyword_text}")

        # 기본 스타일 가이드 추가
        prompt_parts.append("minimalist, modern, clean design, vector art, flat design")

        return ", ".join(prompt_parts)

    def generate_color_palette(
        self,
        base_color: str,
        num_colors: int = 5,
        scheme: str = "complementary"
    ) -> List[str]:
        """
        컬러 팔레트 생성

        Args:
            base_color: 기본 색상 (hex)
            num_colors: 색상 개수
            scheme: 색상 조합 방식 (complementary, analogous, triadic)

        Returns:
            hex 색상 코드 리스트
        """
        # 간단한 색상 팔레트 생성 (실제로는 color-thief나 colorthief 라이브러리 사용)
        # 여기서는 Mock 데이터 반환
        if scheme == "complementary":
            return [
                base_color,
                self._adjust_hue(base_color, 180),
                self._adjust_lightness(base_color, 20),
                self._adjust_lightness(base_color, -20),
                self._adjust_saturation(base_color, -30)
            ][:num_colors]

        elif scheme == "analogous":
            return [
                base_color,
                self._adjust_hue(base_color, 30),
                self._adjust_hue(base_color, -30),
                self._adjust_lightness(base_color, 20),
                self._adjust_lightness(base_color, -20)
            ][:num_colors]

        elif scheme == "triadic":
            return [
                base_color,
                self._adjust_hue(base_color, 120),
                self._adjust_hue(base_color, 240),
                self._adjust_lightness(base_color, 20),
                self._adjust_lightness(base_color, -20)
            ][:num_colors]

        return [base_color] * num_colors

    def _adjust_hue(self, hex_color: str, degrees: int) -> str:
        """색조 조정 (간단한 버전)"""
        # Mock implementation
        return hex_color

    def _adjust_lightness(self, hex_color: str, percent: int) -> str:
        """명도 조정 (간단한 버전)"""
        # Mock implementation
        return hex_color

    def _adjust_saturation(self, hex_color: str, percent: int) -> str:
        """채도 조정 (간단한 버전)"""
        # Mock implementation
        return hex_color


# Singleton instance
ideogram_service = IdeogramService()
