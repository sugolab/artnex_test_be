# ArtNex MVP 개발 핵심 가이드
**Claude CLI 기반 빠른 개발을 위한 핵심 요약**

---

## 🎯 프로젝트 핵심 정보

### 기본 정보
- **프로젝트**: ArtNex (제조업 AI 마케팅 SaaS)
- **개발기간**: 2025-10-23 ~ 2025-12-15 (49일)
- **팀 구성**: Backend 3명 (병렬 개발)
- **목표**: 브랜드 진단 → 디자인 생성 → 마케팅 실행 → 리포트 자동화

### 핵심 KPI
- AI 응답: ≤5초
- 페이지 로드: ≤2초  
- 테스트 커버리지: ≥80%
- API 응답: ≤200ms

---

## 🛠 필수 기술 스택

### Backend 핵심
```yaml
언어: Python 3.11.9
프레임워크: FastAPI 0.115.0
DB: PostgreSQL 15.8 + SQLAlchemy 2.0.35
캐시: Redis 7.4.1
AI: OpenAI API 1.54.3, Ideogram API 1.0
문서: ReportLab 4.2.5 (PDF)
인프라: AWS (EC2, S3, Lambda)
```

### 프로젝트 구조
```
artnex-backend/
├── app/
│   ├── api/v1/endpoints/     # API 엔드포인트
│   ├── core/                 # 설정, 보안
│   ├── models/               # SQLAlchemy 모델
│   ├── schemas/              # Pydantic 스키마
│   ├── services/             # 비즈니스 로직
│   ├── repositories/         # 데이터 접근
│   ├── utils/                # 유틸리티
│   └── main.py               # FastAPI 앱
├── alembic/                  # DB 마이그레이션
├── tests/                    # 테스트
└── requirements/             # 의존성
```

---

## 📐 개발 필수 규칙

### 1. Python 코딩 표준
```python
# 타입 힌트 필수
def create_brand(brand_id: int, data: dict) -> Brand:
    """모든 함수에 타입 힌트와 독스트링 작성"""
    pass

# Pydantic으로 데이터 검증
class BrandCreate(BaseModel):
    brand_name: str = Field(..., min_length=1, max_length=200)
    category: str
    slogan: Optional[str] = None
```

### 2. API 설계 규칙
```python
# RESTful 표준
GET    /api/v1/brands           # 목록 조회
POST   /api/v1/brands           # 생성
GET    /api/v1/brands/{id}      # 단일 조회
PATCH  /api/v1/brands/{id}      # 부분 수정
DELETE /api/v1/brands/{id}      # 삭제

# 표준 응답 형식
{
    "success": true,
    "message": "성공",
    "data": {...},
    "meta": {"page": 1, "total": 100}
}
```

### 3. 보안 필수사항
```python
# 환경변수 사용 (하드코딩 절대 금지)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    secret_key: str
    
    class Config:
        env_file = ".env"

# JWT 인증
from app.core.security import verify_token, get_current_user

@router.get("/brands")
async def list_brands(
    current_user: User = Depends(get_current_user)
):
    pass
```

---

## 🗄 핵심 데이터 구조

### 주요 테이블
```sql
-- 사용자
users (id, email, password_hash, name, role_id)

-- 브랜드 (핵심)
brands (id, user_id, brand_name, category, keywords, logo_url)

-- 브랜드 KPI
brand_kpis (id, brand_id, kpi_type, value, measurement_date)

-- 브랜드 리포트
brand_reports (id, brand_id, report_type, overall_score, ai_summary, pdf_url)

-- 캠페인
campaigns (id, brand_id, campaign_name, budget, start_date, end_date, status)

-- 디자인 프로젝트
design_projects (id, brand_id, tone_manner, color_palette, prompt)
```

### 관계도
```
Users → Brands → Brand_KPIs
              → Brand_Reports
              → Campaigns
              → Design_Projects
              → Content_Trackings
```

---

## 🤖 AI 통합 핵심

### GPT API 기본 패턴
```python
from openai import AsyncOpenAI

class GPTService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-turbo-preview"
    
    async def analyze_market(self, keywords: List[str], industry: str) -> dict:
        """시장 분석"""
        prompt = f"{industry} 산업의 {', '.join(keywords)} 트렌드 분석"
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "마케팅 전문가"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
```

### Ideogram API 기본 패턴
```python
import httpx

async def generate_brand_image(prompt: str, colors: List[str]) -> str:
    """브랜드 이미지 생성"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.ideogram.ai/v1/generate",
            headers={"Authorization": f"Bearer {IDEOGRAM_KEY}"},
            json={
                "prompt": prompt,
                "style": "design",
                "aspect_ratio": "16:9"
            },
            timeout=60.0
        )
        return response.json()["images"][0]["url"]
```

---

## 🔧 빠른 시작 (Claude CLI용)

### 1. 환경 설정
```bash
# .env 파일 생성
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/artnex
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-your-key
IDEOGRAM_API_KEY=your-key
SECRET_KEY=your-secret-min-32-chars

# Docker로 DB/Redis 실행
docker-compose up -d db redis

# 의존성 설치
pip install -r requirements/dev.txt

# DB 마이그레이션
alembic upgrade head

# 개발 서버 실행
uvicorn app.main:app --reload
```

### 2. 기본 FastAPI 앱 구조
```python
# app/main.py
from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="ArtNex API",
    version="1.0.0",
    docs_url="/docs"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 3. 기본 CRUD 패턴
```python
# app/api/v1/endpoints/brands.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.post("/brands")
async def create_brand(
    brand_in: BrandCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """브랜드 생성"""
    brand = Brand(**brand_in.dict(), user_id=current_user.id)
    db.add(brand)
    await db.commit()
    await db.refresh(brand)
    return brand

@router.get("/brands")
async def list_brands(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """브랜드 목록"""
    result = await db.execute(
        select(Brand).where(Brand.user_id == current_user.id)
    )
    return result.scalars().all()

@router.get("/brands/{brand_id}")
async def get_brand(
    brand_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """브랜드 조회"""
    brand = await db.get(Brand, brand_id)
    if not brand or brand.user_id != current_user.id:
        raise HTTPException(404, "브랜드를 찾을 수 없습니다")
    return brand
```

---

## 📋 개발 체크리스트

### 모듈별 필수 구현사항

#### ✅ Back1: 브랜드 관리
- [ ] 브랜드 CRUD API (생성/조회/수정/삭제)
- [ ] 브랜드 KPI 자동 계산
- [ ] 프로젝트 관리 (칸반/리스트/캘린더)
- [ ] 계약 관리 (파일 업로드 S3)
- [ ] 콘텐츠 트래킹 (SNS 크롤링)

#### ✅ Back2: 인사이트 & 리포트
- [ ] GPT 기반 브랜드 인사이트
- [ ] 5단계 진단 로직
- [ ] AI 분석 및 점수화
- [ ] PDF 리포트 생성 (ReportLab)
- [ ] ADMIN RBAC (역할 기반 접근제어)

#### ✅ Back3: 디자인 & 캠페인
- [ ] Ideogram API 디자인 생성
- [ ] 숏폼 스토리보드 자동 생성
- [ ] 캠페인 생성 및 관리
- [ ] 캠페인 성과 리포트
- [ ] 데이터 시각화 (Chart.js)

---

## 🧪 테스트 필수사항

### 단위 테스트 기본
```python
# tests/test_brand_service.py
import pytest
from app.services.brand_service import BrandService

@pytest.mark.asyncio
async def test_create_brand(db_session):
    """브랜드 생성 테스트"""
    service = BrandService(db_session)
    
    brand = await service.create_brand(
        user_id=1,
        brand_data={"brand_name": "테스트", "category": "뷰티"}
    )
    
    assert brand.id is not None
    assert brand.brand_name == "테스트"

# 실행
pytest tests/ -v --cov=app --cov-report=term
```

---

## 🚀 배포 (Docker)

### docker-compose.yml 핵심
```yaml
services:
  backend:
    build: .
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/artnex
      - REDIS_URL=redis://redis:6379/0
    depends_on: [db, redis]
  
  db:
    image: postgres:15.8
    environment:
      POSTGRES_DB: artnex_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes: [pgdata:/var/lib/postgresql/data]
  
  redis:
    image: redis:7.4.1
    volumes: [redisdata:/data]
```

### 배포 명령어
```bash
# 빌드 및 실행
docker-compose up -d

# 마이그레이션
docker-compose exec backend alembic upgrade head

# 로그 확인
docker-compose logs -f backend
```

---

## ⚠️ 핵심 주의사항

### 절대 금지
```python
# ❌ 절대 금지
DATABASE_URL = "postgresql://user:password@localhost/db"  # 하드코딩
logger.info(f"비밀번호: {password}")  # 민감정보 로깅
query = f"SELECT * FROM users WHERE email = '{email}'"  # SQL 인젝션

# ✅ 올바른 방법
from pydantic_settings import BaseSettings
settings = Settings()  # 환경변수 사용
logger.info(f"사용자 {user_id} 인증 시도")  # 안전한 로깅
query = select(User).where(User.email == email)  # 파라미터화
```

### 성능 최적화
```python
# ❌ N+1 쿼리 문제
brands = await db.execute(select(Brand))
for brand in brands:
    kpis = await db.execute(select(KPI).where(KPI.brand_id == brand.id))

# ✅ Eager Loading
from sqlalchemy.orm import selectinload
brands = await db.execute(
    select(Brand).options(selectinload(Brand.kpis))
)
```

### 에러 처리
```python
# ✅ 구체적인 예외 처리
from fastapi import HTTPException

try:
    brand = await service.create_brand(data)
except IntegrityError:
    raise HTTPException(400, "중복된 브랜드명")
except ValueError as e:
    raise HTTPException(400, str(e))
except Exception as e:
    logger.exception(f"예상치 못한 오류: {e}")
    raise HTTPException(500, "서버 오류")
```

---

## 📚 참조 문서 위치

### 프로젝트 문서
- WBS: `/mnt/project/수고랩아트넥스_WBS.pdf`
- PRD: `/mnt/project/수고랩PRD_20251021_v1_0.pdf`
- 기능명세: `/mnt/project/수고랩기능명세서_20251021_v1_0.pdf`
- 개발명세: `/mnt/project/수고랩개발명세서_20251021_v1_0.pdf`
- ERD: `/mnt/project/수고랩ERD_20251021_v1_0.pdf`

### API 문서
- OpenAI: https://platform.openai.com/docs
- Ideogram: https://ideogram.ai/api/docs
- YouTube: https://developers.google.com/youtube/v3

---

## 🎯 일일 개발 루틴

### 작업 시작
1. GitHub Issue 선택
2. 브랜치 생성: `feature/back1-brand-crud`
3. 테스트 작성 (TDD)
4. 구현
5. 로컬 테스트 실행
6. 커밋: `feat(brand): 브랜드 CRUD API 구현`
7. PR 생성

### 코드 리뷰 체크포인트
- [ ] PEP 8 준수
- [ ] 타입 힌트 완성
- [ ] 독스트링 작성
- [ ] 단위 테스트 존재 (커버리지 80%+)
- [ ] API 문서화 (Swagger)
- [ ] 에러 핸들링 완비
- [ ] 보안 검증

---

## 💡 자주 사용하는 명령어

```bash
# 개발 서버
uvicorn app.main:app --reload --port 8000

# 테스트
pytest tests/ -v --cov=app --cov-report=html

# 마이그레이션
alembic revision --autogenerate -m "테이블 추가"
alembic upgrade head
alembic downgrade -1

# 코드 포맷팅
black app/
isort app/
flake8 app/

# Docker
docker-compose up -d
docker-compose logs -f backend
docker-compose exec backend bash
docker-compose down -v

# Git
git checkout -b feature/back1-brand-crud
git commit -m "feat(brand): 브랜드 생성 API 구현"
git push origin feature/back1-brand-crud
```

---

**이 문서는 Claude CLI로 MVP를 빠르게 개발하기 위한 핵심 가이드입니다.**
**더 자세한 내용은 CLAUDE_KR.md를 참조하세요.**