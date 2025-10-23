# ArtNex Platform - Claude Code Development Instructions

**Project**: ArtNex (아트넥스)
**Type**: AI-Powered Brand·Design·Marketing Integrated SaaS Platform for Manufacturing Industry
**Version**: MVP 1.0
**Document Version**: 2.0
**Last Updated**: 2025-10-23
**Development Period**: 2025-10-23 ~ 2025-12-15 (49 development days, 5 test/deploy days)

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Tech Stack & Versions](#-tech-stack--versions)
3. [Development Rules](#-development-rules)
4. [Development Workflow](#-development-workflow)
5. [Critical Attention Points](#-critical-attention-points)
6. [Architecture & Design](#-architecture--design)
7. [Backend Development Guide](#-backend-development-guide)
8. [Database Schema Reference](#-database-schema-reference)
9. [API Development Standards](#-api-development-standards)
10. [AI Integration Guide](#-ai-integration-guide)
11. [Security & Authentication](#-security--authentication)
12. [Testing Strategy](#-testing-strategy)
13. [Deployment Guide](#-deployment-guide)
14. [Team Structure & Responsibilities](#-team-structure--responsibilities)

---

## 🎯 Project Overview

### Core Objective
Build an **AI-powered one-stop platform** that automates the entire workflow from brand diagnosis → design generation → marketing execution → performance reporting for manufacturing companies.

### Key Goals
- **Business Goal**: Improve marketing ROI and market competitiveness for manufacturing companies
- **User Goal**: Provide one-stop workflow from brand registration to report output
- **Technical Goal**: Reduce AI-based report generation time to within 5 minutes

### Success Metrics (KPIs)
| Metric Type | Target | Measurement |
|-------------|--------|-------------|
| User Retention Rate | ≥70% | Monthly active users retention |
| Monthly Active Users (MAU) | 1,000 users | Target user base |
| AI Response Time | ≤5 seconds | GPT/Ideogram API latency |
| Page Load Time | ≤2 seconds | Frontend performance |
| Brand Registration Time | ≤5 minutes | User experience efficiency |

---

## 🛠 Tech Stack & Versions

### Backend Stack

#### Core Framework
```yaml
Language: Python 3.11.9 (LTS)
Framework: FastAPI 0.115.0
ASGI Server: Uvicorn 0.32.0
Data Validation: Pydantic 2.9.2
File Upload: python-multipart 0.0.12
```

#### Database & ORM
```yaml
Primary DB: PostgreSQL 15.8
ORM: SQLAlchemy 2.0.35
Migration: Alembic 1.13.3
Async Driver: asyncpg 0.29.0
Sync Driver: psycopg2-binary 2.9.9
```

#### Caching Layer
```yaml
Cache Server: Redis 7.4.1
Python Client: redis 5.1.1
High-Performance Parser: hiredis 3.0.0
```

#### AI & Machine Learning
```yaml
OpenAI API: 1.54.3
  Models: gpt-4-turbo-preview, gpt-4-1106-preview
Ideogram API: 1.0
scikit-learn: 1.5.2  # Keyword clustering, data analysis
scipy: 1.14.1        # Statistical analysis, KPI calculation
numpy: 2.1.3         # Numerical operations
pandas: 2.2.3        # Data processing
```

#### Document Processing & Generation
```yaml
PDF Generation: ReportLab 4.2.5
Image Processing: Pillow 11.0.0
Word Documents: python-docx 1.1.2
Excel Files: openpyxl 3.1.5
```

#### HTTP Clients & Crawling
```yaml
Async HTTP: httpx 0.27.2, aiohttp 3.10.10
Sync HTTP: requests 2.32.3
HTML Parsing: beautifulsoup4 4.12.3, lxml 5.3.0
YouTube API: google-api-python-client 2.149.0
```

#### Security & Authentication
```yaml
JWT Tokens: python-jose 3.3.0
Password Hashing: passlib 1.7.4, bcrypt 4.2.0
Encryption: cryptography 43.0.3
```

#### AWS SDK
```yaml
AWS SDK: boto3 1.35.54
Core Functions: botocore 1.35.54
```

#### Task Queue & Background Jobs
```yaml
Task Queue: Celery 5.4.0
Monitoring: Flower 2.0.1
```

#### Testing Framework
```yaml
Test Framework: pytest 8.3.3
Async Testing: pytest-asyncio 0.24.0
Code Coverage: pytest-cov 5.0.0
Test Data: faker 30.8.2
```

#### Code Quality Tools
```yaml
Code Formatter: black 24.10.0
Linter: flake8 7.1.1
Type Checker: mypy 1.13.0
Import Sorter: isort 5.13.2
Code Analyzer: pylint 3.3.1
```

#### Logging & Monitoring
```yaml
Advanced Logging: loguru 0.7.2
Error Tracking: sentry-sdk 2.17.0
Metrics Collection: prometheus-client 0.21.0
```

#### Utilities
```yaml
Environment Variables: python-dotenv 1.0.1
Settings Management: pydantic-settings 2.6.1
```

### Frontend Stack (Reference)
```yaml
Framework: Vue.js 3.5.11
Router: Vue Router 4.4.5
State Management: Pinia 2.2.4
CSS Framework: Tailwind CSS 3.4.14
UI Components: Headless UI 2.1.9, Heroicons 2.1.5
Charts: Chart.js 4.4.6, vue-chartjs 5.3.1, Recharts 2.13.0
HTTP Client: axios 1.7.7
Build Tool: Vite 5.4.10
Language: TypeScript 5.6.3
```

### Infrastructure & Deployment

#### AWS Cloud Services
```yaml
EC2: t3.medium (Main Application Server)
  OS: Ubuntu 22.04 LTS
  vCPU: 2
  RAM: 4GB

S3: artnex-mvp-files
  Region: ap-northeast-2 (Seoul)
  Purpose: File storage (contracts, PDFs, design outputs)

Lambda: Python 3.11 runtime
  Memory: 512MB - 1024MB
  Timeout: 30s - 300s
  Purpose: AI computation offloading

RDS PostgreSQL: 15.8
  Development: db.t3.micro
  Production: db.t3.medium

ElastiCache Redis: 7.4.1
  Development: cache.t3.micro
  Production: cache.t3.small

CloudFront: CDN for static file delivery

CloudWatch: Logging and monitoring
```

#### Containerization
```yaml
Docker: 27.3.1
Docker Compose: 2.29.7
Base Image: python:3.11-slim-bookworm
```

#### CI/CD
```yaml
Version Control: Git
Workflow Automation: GitHub Actions
Deployment Automation: AWS CodeDeploy (optional)
```

#### Web Server & Proxy
```yaml
Reverse Proxy: Nginx 1.27.2
Static File Serving: Nginx
SSL/TLS: Let's Encrypt
```

#### DNS & Domain
```yaml
DNS Management: AWS Route 53
```

---

## 📐 Development Rules

### Python Coding Standards

#### PEP 8 Compliance
```python
# Indentation: 4 spaces
# Function names: snake_case
# Class names: PascalCase
# Constants: UPPER_CASE

# Good Examples
def calculate_brand_kpi(brand_id: int) -> float:
    """Calculate KPI for a brand."""
    pass

class BrandManager:
    """Manages brand operations."""
    MAX_BRANDS_PER_USER = 100
```

#### Type Hints (Mandatory)
```python
# All functions MUST have type hints
from typing import List, Dict, Optional
from datetime import datetime

def get_brand_by_id(brand_id: int) -> Optional[Dict[str, any]]:
    """
    Retrieve brand information by ID.

    Args:
        brand_id: The unique identifier of the brand

    Returns:
        Brand data dictionary or None if not found
    """
    pass

async def create_campaign(
    brand_id: int,
    campaign_data: Dict[str, any]
) -> int:
    """Create a new campaign and return its ID."""
    pass
```

#### Docstrings (Google Style)
```python
def analyze_market_trend(
    keywords: List[str],
    date_range: tuple[datetime, datetime]
) -> Dict[str, float]:
    """
    Analyze market trends based on keywords.

    Args:
        keywords: List of search keywords
        date_range: Tuple of (start_date, end_date)

    Returns:
        Dictionary mapping keywords to trend scores

    Raises:
        ValueError: If date_range is invalid
        APIError: If external API call fails

    Example:
        >>> analyze_market_trend(
        ...     ['vegan skincare'],
        ...     (datetime(2025, 1, 1), datetime(2025, 1, 31))
        ... )
        {'vegan skincare': 0.85}
    """
    pass
```

### API Design Principles

#### RESTful Standards
```python
# GET: Retrieve resources
@router.get("/api/v1/brands/{brand_id}")
async def get_brand(brand_id: int):
    """Retrieve a single brand."""
    pass

# POST: Create new resources
@router.post("/api/v1/brands")
async def create_brand(brand: BrandCreate):
    """Create a new brand."""
    pass

# PUT/PATCH: Update existing resources
@router.put("/api/v1/brands/{brand_id}")
async def update_brand(brand_id: int, brand: BrandUpdate):
    """Update brand information."""
    pass

# DELETE: Remove resources
@router.delete("/api/v1/brands/{brand_id}")
async def delete_brand(brand_id: int):
    """Delete a brand."""
    pass
```

#### Version Management
```python
# All APIs MUST use versioning: /api/v1/...
API_VERSION_PREFIX = "/api/v1"

# Future versions will use /api/v2/, etc.
```

#### Error Handling
```python
from fastapi import HTTPException, status

# Use appropriate HTTP status codes
if not brand:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Brand with ID {brand_id} not found"
    )

if not user.has_permission("edit_brand"):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient permissions to edit brand"
    )
```

#### Response Format Standardization
```python
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: str
    error: Optional[Dict[str, any]] = None

# Success response
@router.get("/api/v1/brands")
async def list_brands():
    brands = await get_all_brands()
    return APIResponse(
        success=True,
        data=brands,
        message="Brands retrieved successfully"
    )

# Error response
@router.post("/api/v1/brands")
async def create_brand(brand: BrandCreate):
    try:
        brand_id = await create_new_brand(brand)
        return APIResponse(
            success=True,
            data={"brand_id": brand_id},
            message="Brand created successfully"
        )
    except Exception as e:
        return APIResponse(
            success=False,
            message="Failed to create brand",
            error={"type": type(e).__name__, "details": str(e)}
        )
```

### Git Workflow

#### Branch Strategy
```bash
# Main branches
main         # Production branch (stable releases only)
develop      # Development branch (integration)

# Feature branches
feature/user-authentication
feature/brand-kpi-calculation
feature/ai-report-generation

# Hotfix branches
hotfix/urgent-security-patch
hotfix/api-rate-limiting-bug
```

#### Commit Message Convention
```bash
# Format: [Module] Action description

# Examples:
git commit -m "[Brand] Add KPI auto-calculation API"
git commit -m "[Report] Fix PDF export encoding issue"
git commit -m "[Auth] Implement JWT refresh token logic"
git commit -m "[Campaign] Update budget recommendation algorithm"

# Types of actions:
# Add: New feature
# Update: Enhancement to existing feature
# Fix: Bug fix
# Refactor: Code restructuring
# Remove: Delete deprecated code
# Docs: Documentation only
```

#### Pull Request Requirements
- **Code Review**: Mandatory (minimum 1 approval)
- **Testing**: All tests must pass
- **Coverage**: Maintain >80% code coverage
- **Documentation**: Update relevant docs
- **Breaking Changes**: Clearly documented

### File & Folder Structure
```
/artnex
├── /app
│   ├── /api
│   │   └── /v1
│   │       ├── /routers      # API endpoints
│   │       │   ├── brands.py
│   │       │   ├── campaigns.py
│   │       │   ├── reports.py
│   │       │   └── insights.py
│   │       └── /dependencies  # Shared dependencies
│   ├── /models               # Pydantic models & DB models
│   │   ├── /database        # SQLAlchemy models
│   │   └── /schemas         # Pydantic schemas
│   ├── /services            # Business logic layer
│   │   ├── brand_service.py
│   │   ├── ai_service.py
│   │   └── report_service.py
│   ├── /core                # Core configurations
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── /utils               # Utility functions
│   └── main.py              # FastAPI application entry
├── /tests
│   ├── /unit
│   ├── /integration
│   └── /e2e
├── /alembic                 # Database migrations
├── /docker
├── /nginx
├── /scripts
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

---

## 🔄 Development Workflow

### Daily Development Cycle

#### 1. Morning Standup (Async/Sync)
- Review yesterday's accomplishments
- Identify today's priorities (based on WBS)
- Flag any blockers or dependencies

#### 2. Development Session
```bash
# 1. Pull latest changes
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/brand-kpi-calculation

# 3. Develop with test-driven approach
# Write test first
vim tests/test_brand_service.py

# Implement feature
vim app/services/brand_service.py

# Run tests
pytest tests/test_brand_service.py -v

# 4. Commit frequently
git add .
git commit -m "[Brand] Add KPI calculation logic"

# 5. Push and create PR
git push origin feature/brand-kpi-calculation
```

#### 3. Code Review Process
1. Create Pull Request with description
2. Request review from team member
3. Address review comments
4. Get approval
5. Merge to `develop` branch

#### 4. Integration Testing
- Run full test suite on `develop` branch
- Verify API endpoints with Postman/Swagger
- Check database migrations

### Sprint Planning (Weekly)

#### Week Structure
- **Monday**: Sprint planning, task assignment
- **Tuesday-Thursday**: Development sprint
- **Friday**: Code review, integration testing, retrospective

#### Task Master AI Workflow
```bash
# Initialize project (First time only)
tm init

# Add tasks for the week
tm add "Implement brand KPI calculation API"
tm add "Integrate Ideogram API for design generation"
tm add "Create campaign budget recommendation algorithm"

# Track progress
tm next          # Get next task
tm status 1 done # Mark task as complete
tm list          # View all tasks

# Generate weekly report
tm report
```

### Testing Workflow

#### Unit Testing
```python
# File: tests/unit/test_brand_service.py
import pytest
from app.services.brand_service import calculate_kpi

def test_calculate_kpi_valid_brand():
    """Test KPI calculation with valid brand data."""
    result = calculate_kpi(brand_id=1)
    assert result > 0
    assert isinstance(result, float)

def test_calculate_kpi_invalid_brand():
    """Test KPI calculation with non-existent brand."""
    with pytest.raises(ValueError):
        calculate_kpi(brand_id=99999)
```

#### Integration Testing
```python
# File: tests/integration/test_brand_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_brand_endpoint():
    """Test brand creation API endpoint."""
    brand_data = {
        "brand_name": "Test Brand",
        "category": "Beauty",
        "slogan": "Test Slogan"
    }
    response = client.post("/api/v1/brands", json=brand_data)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "brand_id" in response.json()["data"]
```

#### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_brand_service.py -v

# Run tests matching pattern
pytest -k "test_brand" -v
```

---

## ⚠️ Critical Attention Points

### 🚨 High Priority Alerts

#### 1. AI Response Time Constraint
```python
# CRITICAL: All AI operations MUST complete within 5 seconds
import asyncio
from functools import wraps

def timeout(seconds=5):
    """Decorator to enforce timeout on AI operations."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError:
                raise APIError(f"AI operation exceeded {seconds}s timeout")
        return wrapper
    return decorator

@timeout(seconds=5)
async def generate_brand_insight(prompt: str):
    """Generate brand insight with timeout protection."""
    # GPT API call with timeout
    pass
```

#### 2. Database Performance
```python
# CRITICAL: Always use indexed columns for queries
# ❌ BAD: Full table scan
brands = await db.query(Brand).filter(Brand.category == "Beauty").all()

# ✅ GOOD: Use indexed column with proper indexing
# Ensure index exists: CREATE INDEX idx_brands_category ON brands(category);
brands = await db.query(Brand).filter(Brand.category == "Beauty").all()

# CRITICAL: Use pagination for large result sets
# ❌ BAD: Load all brands at once
all_brands = await db.query(Brand).all()

# ✅ GOOD: Implement pagination
def get_brands_paginated(skip: int = 0, limit: int = 20):
    return db.query(Brand).offset(skip).limit(limit).all()
```

#### 3. Security Requirements
```python
# CRITICAL: Never expose sensitive data
# ❌ BAD: Return password hash
@router.get("/api/v1/users/{user_id}")
async def get_user(user_id: int):
    user = await db.query(User).filter(User.id == user_id).first()
    return user  # Contains password_hash!

# ✅ GOOD: Use response model to exclude sensitive fields
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    # password_hash excluded

@router.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await db.query(User).filter(User.id == user_id).first()
    return user

# CRITICAL: Always validate and sanitize inputs
from pydantic import validator

class BrandCreate(BaseModel):
    brand_name: str
    category: str

    @validator('brand_name')
    def validate_brand_name(cls, v):
        if len(v) < 2 or len(v) > 200:
            raise ValueError('Brand name must be 2-200 characters')
        if not v.strip():
            raise ValueError('Brand name cannot be empty')
        return v.strip()
```

#### 4. Error Handling & Logging
```python
# CRITICAL: Log all errors with context
from loguru import logger

@router.post("/api/v1/brands")
async def create_brand(brand: BrandCreate):
    try:
        brand_id = await create_new_brand(brand)
        logger.info(f"Brand created successfully: {brand_id}")
        return {"success": True, "brand_id": brand_id}
    except Exception as e:
        logger.error(f"Failed to create brand: {brand.brand_name}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to create brand. Please try again."
        )
```

### 🔒 Security Critical Points

#### API Key Management
```python
# CRITICAL: Never commit API keys to git
# ❌ BAD
OPENAI_API_KEY = "sk-1234567890abcdef"

# ✅ GOOD: Use environment variables
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    IDEOGRAM_API_KEY: str
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
```

#### SQL Injection Prevention
```python
# CRITICAL: Use ORM to prevent SQL injection
# ❌ BAD: String concatenation
def get_brand_by_name(name: str):
    query = f"SELECT * FROM brands WHERE brand_name = '{name}'"
    return db.execute(query)

# ✅ GOOD: Use ORM parameterized queries
def get_brand_by_name(name: str):
    return db.query(Brand).filter(Brand.brand_name == name).first()
```

#### CORS Configuration
```python
# CRITICAL: Restrict CORS to specific origins in production
from fastapi.middleware.cors import CORSMiddleware

# ❌ BAD: Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dangerous!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ GOOD: Whitelist specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://artnex.com",
        "https://www.artnex.com",
        "https://app.artnex.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### 🎯 Performance Critical Points

#### Database Connection Pooling
```python
# CRITICAL: Use connection pooling for production
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,        # CRITICAL: Adjust based on load
    max_overflow=40,     # CRITICAL: Allow burst connections
    pool_pre_ping=True,  # CRITICAL: Check connections before use
    pool_recycle=3600    # CRITICAL: Recycle connections hourly
)
```

#### Redis Caching Strategy
```python
# CRITICAL: Cache expensive operations
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expiration=3600):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expiration, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_result(expiration=1800)  # Cache for 30 minutes
async def get_dashboard_stats(brand_id: int):
    """Expensive dashboard statistics calculation."""
    # Heavy computation here
    pass
```

---

## 🏗 Architecture & Design

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Layer                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Browser   │  │   Mobile    │  │   Desktop   │            │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
│         │                 │                 │                    │
└─────────┼─────────────────┼─────────────────┼────────────────────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CDN Layer (CloudFront)                      │
│                     Static Assets Delivery                        │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Load Balancer / Nginx                          │
│              SSL Termination + Reverse Proxy                     │
└─────────────────────────────────────────────────────────────────┘
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
          ▼                                   ▼
┌──────────────────────┐            ┌──────────────────────┐
│  Frontend (Vue.js)   │            │  Backend (FastAPI)   │
│  ─────────────────   │            │  ─────────────────   │
│  • Vue Router        │◄───────────►  • REST API         │
│  • Pinia Store       │            │  • JWT Auth          │
│  • Tailwind CSS      │            │  • Business Logic    │
│  • Chart.js          │            │  • Data Validation   │
└──────────────────────┘            └──────────┬───────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    │                         │                         │
                    ▼                         ▼                         ▼
          ┌────────────────────┐   ┌────────────────────┐   ┌────────────────────┐
          │   PostgreSQL DB    │   │   Redis Cache      │   │   AWS Services     │
          │   ──────────────   │   │   ──────────────   │   │   ──────────────   │
          │   • Brands         │   │   • Sessions       │   │   • S3 (Files)     │
          │   • Campaigns      │   │   • Dashboard      │   │   • Lambda (AI)    │
          │   • Reports        │   │   • API Cache      │   │   • CloudWatch     │
          └────────────────────┘   └────────────────────┘   └────────────────────┘
                                              │
                                              ▼
                                   ┌────────────────────┐
                                   │   AI Services      │
                                   │   ──────────────   │
                                   │   • GPT-4 API      │
                                   │   • Ideogram API   │
                                   │   • YouTube API    │
                                   └────────────────────┘
```

### Multi-Layer Architecture

#### 1. Presentation Layer (Vue.js Frontend)
- **Responsibility**: User interface, user interaction, client-side validation
- **Technology**: Vue 3, Tailwind CSS, Chart.js
- **Communication**: REST API calls to backend

#### 2. API Gateway Layer (FastAPI)
- **Responsibility**: Request routing, authentication, rate limiting
- **Technology**: FastAPI routers, middleware
- **Security**: JWT validation, RBAC enforcement

#### 3. Business Logic Layer (Services)
- **Responsibility**: Core business logic, workflow orchestration
- **Technology**: Python services, Pydantic validation
- **Examples**: `brand_service.py`, `campaign_service.py`, `ai_service.py`

#### 4. Data Access Layer (SQLAlchemy)
- **Responsibility**: Database operations, query optimization
- **Technology**: SQLAlchemy ORM, Alembic migrations
- **Pattern**: Repository pattern for data access

#### 5. Infrastructure Layer
- **Responsibility**: External services, caching, file storage
- **Technology**: AWS services, Redis, external APIs

### Design Patterns

#### Repository Pattern (Data Access)
```python
# File: app/repositories/brand_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.database.brand import Brand

class BrandRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, brand_id: int) -> Optional[Brand]:
        """Retrieve brand by ID."""
        return await self.db.get(Brand, brand_id)

    async def get_by_user(self, user_id: int) -> List[Brand]:
        """Get all brands owned by a user."""
        result = await self.db.execute(
            select(Brand).filter(Brand.user_id == user_id)
        )
        return result.scalars().all()

    async def create(self, brand_data: dict) -> Brand:
        """Create a new brand."""
        brand = Brand(**brand_data)
        self.db.add(brand)
        await self.db.commit()
        await self.db.refresh(brand)
        return brand
```

#### Service Layer Pattern (Business Logic)
```python
# File: app/services/brand_service.py
from app.repositories.brand_repository import BrandRepository
from app.models.schemas.brand import BrandCreate, BrandResponse

class BrandService:
    def __init__(self, brand_repo: BrandRepository):
        self.brand_repo = brand_repo

    async def create_brand(
        self,
        brand_data: BrandCreate,
        user_id: int
    ) -> BrandResponse:
        """
        Create a new brand with business logic validation.
        """
        # Business logic: Check user brand limit
        existing_brands = await self.brand_repo.get_by_user(user_id)
        if len(existing_brands) >= MAX_BRANDS_PER_USER:
            raise BusinessException("Maximum brand limit reached")

        # Business logic: Generate AI suggestions
        ai_suggestions = await self.generate_ai_suggestions(brand_data)

        # Create brand with enriched data
        brand_dict = brand_data.dict()
        brand_dict['user_id'] = user_id
        brand_dict['ai_suggestions'] = ai_suggestions

        brand = await self.brand_repo.create(brand_dict)
        return BrandResponse.from_orm(brand)
```

#### Dependency Injection (FastAPI)
```python
# File: app/api/v1/routers/brands.py
from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.repositories.brand_repository import BrandRepository
from app.services.brand_service import BrandService

router = APIRouter()

def get_brand_service(db: AsyncSession = Depends(get_db)) -> BrandService:
    """Dependency injection for BrandService."""
    brand_repo = BrandRepository(db)
    return BrandService(brand_repo)

@router.post("/brands", response_model=BrandResponse)
async def create_brand(
    brand: BrandCreate,
    current_user: User = Depends(get_current_user),
    brand_service: BrandService = Depends(get_brand_service)
):
    """Create a new brand."""
    return await brand_service.create_brand(brand, current_user.id)
```

---

## 🔧 Backend Development Guide

### Project Initialization

#### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip==24.3.1
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration
```

#### 2. Database Setup
```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

#### 3. Run Development Server
```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run with workers (production-like)
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Core Module Development

#### 1. Brand Managing Module (Back1 Responsibility)

##### Database Models
```python
# File: app/models/database/brand.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    brand_name = Column(String(200), nullable=False)
    slogan = Column(String(500), nullable=True)
    mission = Column(Text, nullable=True)
    vision = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)
    keywords = Column(JSON, nullable=True)
    logo_url = Column(String(500), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="brands")
    kpis = relationship("BrandKPI", back_populates="brand", cascade="all, delete-orphan")
    personas = relationship("BrandPersona", back_populates="brand", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_brands_user_id', 'user_id'),
        Index('idx_brands_category', 'category'),
    )
```

##### Pydantic Schemas
```python
# File: app/models/schemas/brand.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class BrandBase(BaseModel):
    brand_name: str = Field(..., min_length=2, max_length=200)
    slogan: Optional[str] = Field(None, max_length=500)
    mission: Optional[str] = None
    vision: Optional[str] = None
    category: str = Field(..., max_length=100)
    keywords: Optional[List[str]] = None

    @validator('brand_name')
    def validate_brand_name(cls, v):
        if not v.strip():
            raise ValueError('Brand name cannot be empty')
        return v.strip()

class BrandCreate(BrandBase):
    """Schema for creating a new brand."""
    pass

class BrandUpdate(BaseModel):
    """Schema for updating a brand (all fields optional)."""
    brand_name: Optional[str] = None
    slogan: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    category: Optional[str] = None
    keywords: Optional[List[str]] = None

class BrandResponse(BrandBase):
    """Schema for brand response."""
    id: int
    user_id: int
    logo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

##### API Endpoints
```python
# File: app/api/v1/routers/brands.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.schemas.brand import BrandCreate, BrandUpdate, BrandResponse
from app.services.brand_service import BrandService
from app.api.dependencies import get_current_user, get_brand_service

router = APIRouter(prefix="/api/v1/brands", tags=["brands"])

@router.get("", response_model=List[BrandResponse])
async def list_brands(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    brand_service: BrandService = Depends(get_brand_service)
):
    """
    List all brands for the current user with pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 20)
    """
    return await brand_service.get_user_brands(current_user.id, skip, limit)

@router.post("", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
async def create_brand(
    brand: BrandCreate,
    current_user: User = Depends(get_current_user),
    brand_service: BrandService = Depends(get_brand_service)
):
    """
    Create a new brand.

    - **brand_name**: Name of the brand (required)
    - **category**: Industry category (required)
    - **slogan**: Brand slogan (optional)
    - **mission**: Brand mission statement (optional)
    - **vision**: Brand vision statement (optional)
    """
    return await brand_service.create_brand(brand, current_user.id)

@router.get("/{brand_id}", response_model=BrandResponse)
async def get_brand(
    brand_id: int,
    current_user: User = Depends(get_current_user),
    brand_service: BrandService = Depends(get_brand_service)
):
    """Get brand details by ID."""
    brand = await brand_service.get_brand_by_id(brand_id)

    # Authorization check
    if brand.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this brand"
        )

    return brand

@router.put("/{brand_id}", response_model=BrandResponse)
async def update_brand(
    brand_id: int,
    brand_update: BrandUpdate,
    current_user: User = Depends(get_current_user),
    brand_service: BrandService = Depends(get_brand_service)
):
    """Update brand information."""
    return await brand_service.update_brand(brand_id, brand_update, current_user.id)

@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(
    brand_id: int,
    current_user: User = Depends(get_current_user),
    brand_service: BrandService = Depends(get_brand_service)
):
    """Delete a brand."""
    await brand_service.delete_brand(brand_id, current_user.id)
```

##### KPI Calculation Service
```python
# File: app/services/kpi_service.py
import numpy as np
from scipy import stats
from typing import Dict, List
from app.models.database.brand_kpi import BrandKPI

class KPIService:
    """Service for calculating brand KPIs using scipy."""

    async def calculate_popularity_index(
        self,
        followers: int,
        engagement_rate: float,
        post_count: int,
        views: int
    ) -> float:
        """
        Calculate Popularity Index using weighted formula.

        Formula: PI = (0.3 * normalized_followers) +
                     (0.4 * engagement_rate) +
                     (0.2 * normalized_views) +
                     (0.1 * post_frequency_score)
        """
        # Normalize followers (log scale)
        normalized_followers = np.log10(max(followers, 1)) / 7  # Max 10M followers

        # Normalize views
        normalized_views = np.log10(max(views, 1)) / 8  # Max 100M views

        # Post frequency score (assuming monthly data)
        post_frequency_score = min(post_count / 30, 1.0)  # Cap at 30 posts/month

        # Calculate weighted popularity index
        popularity_index = (
            0.3 * normalized_followers +
            0.4 * min(engagement_rate, 1.0) +
            0.2 * normalized_views +
            0.1 * post_frequency_score
        ) * 100  # Scale to 0-100

        return round(popularity_index, 2)

    async def calculate_trend_score(
        self,
        historical_data: List[float],
        window_size: int = 7
    ) -> float:
        """
        Calculate trend score using linear regression.

        Args:
            historical_data: List of historical values (e.g., daily followers)
            window_size: Number of days to consider for trend

        Returns:
            Trend score: positive for upward trend, negative for downward
        """
        if len(historical_data) < 2:
            return 0.0

        # Take last N days
        data = historical_data[-window_size:]
        x = np.arange(len(data))
        y = np.array(data)

        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        # Normalize slope to -100 to +100 range
        trend_score = np.tanh(slope) * 100

        return round(trend_score, 2)
```

#### 2. Brand Insight Module (Back2 Responsibility)

##### GPT Integration Service
```python
# File: app/services/ai_service.py
import openai
from typing import List, Dict
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

class AIService:
    """Service for AI-powered brand insights using GPT."""

    async def analyze_brand_market(
        self,
        brand_info: Dict[str, any],
        query: str
    ) -> Dict[str, any]:
        """
        Analyze brand market opportunities using GPT-4.

        Args:
            brand_info: Brand information (name, category, target audience)
            query: User's specific query

        Returns:
            AI-generated market analysis
        """
        system_prompt = """
        You are an expert brand marketing consultant specializing in
        manufacturing industry marketing strategies. Provide detailed,
        actionable insights based on market data and trends.
        """

        user_prompt = f"""
        Brand: {brand_info['brand_name']}
        Category: {brand_info['category']}
        Target Audience: {brand_info.get('target_audience', 'General')}

        Question: {query}

        Please provide:
        1. Market opportunity analysis (3-5 specific opportunities)
        2. Recommended product ideas (5-7 items)
        3. Relevant keywords for SEO/marketing
        4. Potential influencer profiles to collaborate with
        5. Market size estimation and growth trends

        Format your response as JSON with keys:
        opportunities, product_ideas, keywords, influencers, market_data
        """

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
                timeout=5.0  # CRITICAL: 5-second timeout
            )

            result = response.choices[0].message.content
            return json.loads(result)

        except openai.error.Timeout:
            raise APIError("AI analysis timed out. Please try again.")
        except json.JSONDecodeError:
            raise AIError("Failed to parse AI response")

    async def cluster_keywords(
        self,
        keywords: List[str],
        num_clusters: int = 5
    ) -> Dict[str, List[str]]:
        """
        Cluster keywords using scikit-learn.

        Args:
            keywords: List of keywords to cluster
            num_clusters: Number of clusters to create

        Returns:
            Dictionary mapping cluster names to keyword lists
        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans

        # Vectorize keywords
        vectorizer = TfidfVectorizer(max_features=100)
        X = vectorizer.fit_transform(keywords)

        # K-Means clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(X)

        # Group keywords by cluster
        clusters = {}
        for idx, label in enumerate(kmeans.labels_):
            cluster_name = f"Cluster_{label + 1}"
            if cluster_name not in clusters:
                clusters[cluster_name] = []
            clusters[cluster_name].append(keywords[idx])

        return clusters
```

#### 3. Design Studio Module (Back3 Responsibility)

##### Ideogram API Integration
```python
# File: app/services/design_service.py
import aiohttp
from typing import Dict, List
from app.core.config import settings

class DesignService:
    """Service for AI-powered design generation using Ideogram API."""

    def __init__(self):
        self.api_key = settings.IDEOGRAM_API_KEY
        self.base_url = "https://api.ideogram.ai/v1"

    async def generate_brand_design(
        self,
        brand_keywords: List[str],
        tone_manner: Dict[str, float],
        color_palette: List[str],
        style: str = "modern"
    ) -> Dict[str, any]:
        """
        Generate brand design using Ideogram API.

        Args:
            brand_keywords: List of brand keywords
            tone_manner: Tone and manner scores (e.g., {"modern": 0.8, "elegant": 0.6})
            color_palette: List of hex color codes
            style: Design style (modern, vintage, minimalist, etc.)

        Returns:
            Generated design with image URL and metadata
        """
        # Build prompt from brand inputs
        prompt = self._build_design_prompt(
            brand_keywords,
            tone_manner,
            color_palette,
            style
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/generate",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "prompt": prompt,
                    "width": 1024,
                    "height": 1024,
                    "style": style,
                    "num_images": 1
                },
                timeout=aiohttp.ClientTimeout(total=5.0)  # 5-second timeout
            ) as response:
                if response.status != 200:
                    raise APIError(f"Ideogram API error: {response.status}")

                result = await response.json()
                return {
                    "image_url": result["images"][0]["url"],
                    "prompt_used": prompt,
                    "color_palette": color_palette,
                    "style": style
                }

    def _build_design_prompt(
        self,
        keywords: List[str],
        tone_manner: Dict[str, float],
        colors: List[str],
        style: str
    ) -> str:
        """Build optimized prompt for Ideogram API."""
        # Extract top tone attributes
        top_tones = sorted(
            tone_manner.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        tone_str = ", ".join([tone for tone, _ in top_tones])

        # Format color palette
        color_str = ", ".join(colors)

        # Construct prompt
        prompt = f"""
        Create a professional brand logo/design with the following specifications:

        Keywords: {", ".join(keywords)}
        Style: {style}
        Tone: {tone_str}
        Color Palette: {color_str}

        Requirements:
        - Clean, modern aesthetic
        - Suitable for digital and print media
        - Professional quality
        - Memorable and distinctive
        """

        return prompt.strip()
```

---

## 🗄 Database Schema Reference

### Entity Relationship Overview

```
Users (1) ──────────────> (N) Brands
                               │
                               ├──> (N) Brand_KPIs
                               ├──> (N) Brand_Personas
                               ├──> (N) Competitors
                               ├──> (N) Projects ──> (N) Contracts
                               ├──> (N) Brand_Reports ──> (N) Report_Sections
                               │                      └──> (N) Brand_Diagnostics
                               ├──> (N) Brand_Insights ──> (N) Insight_Results
                               ├──> (N) Design_Projects ──> (N) Design_Results
                               ├──> (N) Shortform_Projects ──> Shortform_Storyboards ──> Storyboard_Frames
                               ├──> (N) Content_Trackings ──> (N) Tracked_Contents
                               └──> (N) Campaigns ──> (N) Campaign_Influencers
                                            └──> (N) Campaign_Reports
```

### Core Tables Summary

| Module | Table Name | Primary Keys | Foreign Keys | Purpose |
|--------|-----------|--------------|--------------|---------|
| **User Management** | Users | id | role_id → Roles.id | System users |
| | Roles | id | - | User roles and permissions |
| **Brand Management** | Brands | id | user_id → Users.id | Core brand information |
| | Brand_KPIs | id | brand_id → Brands.id | Brand performance metrics |
| | Brand_Personas | id | brand_id → Brands.id | Target persona definitions |
| | Competitors | id | brand_id → Brands.id | Competitor information |
| **Projects & Contracts** | Projects | id | brand_id → Brands.id, user_id → Users.id | Project management |
| | Contracts | id | brand_id → Brands.id, project_id → Projects.id | Contract information |
| **Brand Diagnosis & Reports** | Brand_Reports | id | brand_id → Brands.id | Brand diagnosis reports |
| | Report_Sections | id | report_id → Brand_Reports.id | Report section details |
| | Brand_Diagnostics | id | report_id → Brand_Reports.id | Diagnosis questionnaire data |
| **Brand Insights** | Brand_Insights | id | brand_id → Brands.id | AI insight requests |
| | Insight_Results | id | insight_id → Brand_Insights.id | AI insight results |
| **Design Studio** | Design_Projects | id | brand_id → Brands.id | Design generation projects |
| | Design_Results | id | design_project_id → Design_Projects.id | AI-generated designs |
| **Shortform Studio** | Shortform_Projects | id | brand_id → Brands.id | Shortform video projects |
| | Shortform_Storyboards | id | shortform_project_id → Shortform_Projects.id | Storyboard information |
| | Storyboard_Frames | id | storyboard_id → Shortform_Storyboards.id | Individual storyboard frames |
| **Content Tracking** | Content_Trackings | id | brand_id → Brands.id | Content tracking settings |
| | Tracked_Contents | id | tracking_id → Content_Trackings.id | Tracked content details |
| **Campaign Management** | Campaigns | id | brand_id → Brands.id, user_id → Users.id | Marketing campaigns |
| | Campaign_Influencers | id | campaign_id → Campaigns.id | Campaign influencer information |
| | Campaign_Reports | id | campaign_id → Campaigns.id | Campaign performance reports |

### Critical Indexing Strategy

```sql
-- Brand module indexes (CRITICAL for performance)
CREATE INDEX idx_brands_user_id ON brands(user_id);
CREATE INDEX idx_brands_category ON brands(category);
CREATE INDEX idx_brands_created_at ON brands(created_at);

-- Project module indexes
CREATE INDEX idx_projects_brand_id ON projects(brand_id);
CREATE INDEX idx_projects_status ON projects(status);

-- Campaign module indexes
CREATE INDEX idx_campaigns_brand_id ON campaigns(brand_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_date_range ON campaigns(start_date, end_date);

-- Report module indexes
CREATE INDEX idx_brand_reports_brand_id ON brand_reports(brand_id);
CREATE INDEX idx_brand_reports_created_at ON brand_reports(created_at);

-- Content tracking indexes
CREATE INDEX idx_tracked_contents_tracking_id ON tracked_contents(tracking_id);
CREATE INDEX idx_tracked_contents_platform ON tracked_contents(platform);
CREATE INDEX idx_tracked_contents_published_at ON tracked_contents(published_at);
```

### Sample Table Definition (PostgreSQL)

```sql
-- Brands table (Core entity)
CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    brand_name VARCHAR(200) NOT NULL,
    slogan VARCHAR(500),
    mission TEXT,
    vision TEXT,
    category VARCHAR(100) NOT NULL,
    keywords JSONB,
    logo_url VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_brands_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Brand_KPIs table
CREATE TABLE brand_kpis (
    id SERIAL PRIMARY KEY,
    brand_id INT NOT NULL,
    kpi_type VARCHAR(100) NOT NULL,
    value FLOAT NOT NULL,
    measurement_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_brand_kpis_brand
        FOREIGN KEY (brand_id)
        REFERENCES brands(id)
        ON DELETE CASCADE
);

-- Brand_Reports table
CREATE TABLE brand_reports (
    id SERIAL PRIMARY KEY,
    brand_id INT NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    overall_score FLOAT,
    ai_summary TEXT,
    pdf_url VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_brand_reports_brand
        FOREIGN KEY (brand_id)
        REFERENCES brands(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_overall_score
        CHECK (overall_score >= 0 AND overall_score <= 100)
);
```

---

## 🔌 API Development Standards

### API Endpoint Naming Convention

```python
# RESTful resource-based naming
GET    /api/v1/brands              # List brands
POST   /api/v1/brands              # Create brand
GET    /api/v1/brands/{id}         # Get brand details
PUT    /api/v1/brands/{id}         # Update brand
DELETE /api/v1/brands/{id}         # Delete brand

# Nested resources
GET    /api/v1/brands/{id}/kpis    # List brand KPIs
POST   /api/v1/brands/{id}/kpis    # Create brand KPI

# Action-based endpoints (when RESTful doesn't fit)
POST   /api/v1/brands/{id}/diagnose       # Trigger diagnosis
POST   /api/v1/reports/{id}/export        # Export report
POST   /api/v1/campaigns/{id}/activate    # Activate campaign
```

### Request/Response Standards

#### Standard Success Response
```json
{
  "success": true,
  "data": {
    "brand_id": 123,
    "brand_name": "Vegan Skincare Co.",
    "category": "Beauty"
  },
  "message": "Brand created successfully",
  "meta": {
    "timestamp": "2025-10-23T10:30:00Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "brand_name",
        "message": "Brand name must be at least 2 characters"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-10-23T10:30:00Z",
    "request_id": "req_abc123xyz"
  }
}
```

#### Pagination Response
```json
{
  "success": true,
  "data": [
    {"id": 1, "brand_name": "Brand A"},
    {"id": 2, "brand_name": "Brand B"}
  ],
  "pagination": {
    "total": 50,
    "page": 1,
    "page_size": 20,
    "total_pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

### API Documentation (OpenAPI/Swagger)

```python
# File: app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="ArtNex API",
    description="AI-powered brand marketing automation platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ArtNex API Documentation",
        version="1.0.0",
        description="""
        # ArtNex Platform API

        AI-powered brand marketing automation SaaS platform for manufacturing industry.

        ## Features
        - **Brand Management**: CRUD operations for brands
        - **AI Insights**: Market analysis and recommendations
        - **Design Generation**: AI-powered design creation
        - **Campaign Management**: Marketing campaign orchestration
        - **Performance Reports**: Automated report generation

        ## Authentication
        All endpoints (except `/auth/*`) require JWT Bearer token authentication.

        Example:
        ```
        Authorization: Bearer <your_jwt_token>
        ```
        """,
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### Rate Limiting

```python
# File: app/middleware/rate_limit.py
from fastapi import Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# Apply to FastAPI app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Use in endpoints
@router.post("/api/v1/insights/analyze")
@limiter.limit("5/minute")  # Max 5 requests per minute
async def analyze_insight(request: Request, prompt: str):
    """AI analysis endpoint with rate limiting."""
    pass

@router.get("/api/v1/brands")
@limiter.limit("100/minute")  # Max 100 requests per minute
async def list_brands(request: Request):
    """List brands with higher rate limit."""
    pass
```

---

## 🤖 AI Integration Guide

### GPT API Best Practices

#### Prompt Engineering Principles

1. **Clear Role Definition**
```python
system_prompt = """
You are an expert brand marketing consultant with 15+ years of experience
in the manufacturing industry. You specialize in helping B2B and B2C brands
develop data-driven marketing strategies, identify market opportunities,
and optimize brand positioning.
"""
```

2. **Specific Instructions**
```python
user_prompt = f"""
Analyze the following brand and provide specific, actionable recommendations:

Brand Name: {brand_name}
Industry: {industry}
Target Audience: {target_audience}
Current Challenges: {challenges}

Please provide:
1. Three specific market opportunities with estimated TAM
2. Five product ideas with unique value propositions
3. Ten SEO/marketing keywords ranked by search volume
4. Five potential influencer profiles (with follower ranges)
5. Competitive positioning strategy

Format: Respond in JSON format with keys: opportunities, product_ideas,
keywords, influencers, positioning_strategy
"""
```

3. **Output Format Specification**
```python
# Always specify exact JSON structure
response_format = {
    "opportunities": [
        {
            "title": "string",
            "description": "string",
            "estimated_tam": "number",
            "confidence": "number (0-1)"
        }
    ],
    "product_ideas": [
        {
            "name": "string",
            "description": "string",
            "target_segment": "string",
            "unique_value_prop": "string"
        }
    ],
    # ... etc
}
```

4. **Temperature and Token Control**
```python
# For factual analysis: Low temperature
response = await openai.ChatCompletion.acreate(
    model="gpt-4-turbo-preview",
    temperature=0.3,  # Low for consistency
    max_tokens=1000
)

# For creative suggestions: Higher temperature
response = await openai.ChatCompletion.acreate(
    model="gpt-4-turbo-preview",
    temperature=0.8,  # Higher for creativity
    max_tokens=1500
)
```

### Ideogram API Integration

#### Image Generation Strategy

```python
# File: app/services/design_service.py

async def generate_brand_image(
    self,
    brand_data: Dict[str, any],
    design_type: str = "logo"
) -> Dict[str, any]:
    """
    Generate brand image with optimized parameters.

    Args:
        brand_data: Brand information (keywords, colors, tone)
        design_type: Type of design (logo, banner, product_mockup)

    Returns:
        Generated image URL and metadata
    """
    # Build optimized prompt
    prompt = self._build_image_prompt(brand_data, design_type)

    # Determine optimal dimensions
    dimensions = self._get_optimal_dimensions(design_type)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{self.base_url}/generate",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt,
                "negative_prompt": "blurry, low quality, distorted, watermark",
                "width": dimensions["width"],
                "height": dimensions["height"],
                "style_preset": brand_data.get("style", "modern"),
                "num_inference_steps": 50,  # Quality vs speed trade-off
                "guidance_scale": 7.5       # Adherence to prompt
            },
            timeout=aiohttp.ClientTimeout(total=5.0)
        ) as response:
            result = await response.json()
            return result

def _get_optimal_dimensions(self, design_type: str) -> Dict[str, int]:
    """Get optimal image dimensions based on design type."""
    dimensions_map = {
        "logo": {"width": 1024, "height": 1024},
        "banner": {"width": 1920, "height": 1080},
        "product_mockup": {"width": 1024, "height": 1024},
        "social_media_post": {"width": 1080, "height": 1080},
        "story": {"width": 1080, "height": 1920}
    }
    return dimensions_map.get(design_type, {"width": 1024, "height": 1024})
```

### YouTube API for Content Tracking

```python
# File: app/services/content_tracking_service.py
from googleapiclient.discovery import build
from typing import List, Dict

class ContentTrackingService:
    """Service for tracking content on social media platforms."""

    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

    async def search_youtube_videos(
        self,
        keywords: List[str],
        max_results: int = 50,
        date_range: tuple = None
    ) -> List[Dict[str, any]]:
        """
        Search YouTube videos by keywords.

        Args:
            keywords: List of search keywords
            max_results: Maximum number of results to return
            date_range: Optional tuple of (start_date, end_date)

        Returns:
            List of video metadata
        """
        search_query = " ".join(keywords)

        request_params = {
            'part': 'snippet,statistics',
            'q': search_query,
            'type': 'video',
            'maxResults': max_results,
            'order': 'relevance'
        }

        # Add date filter if provided
        if date_range:
            start_date, end_date = date_range
            request_params['publishedAfter'] = start_date.isoformat() + 'Z'
            request_params['publishedBefore'] = end_date.isoformat() + 'Z'

        # Execute search
        response = self.youtube.search().list(**request_params).execute()

        # Process results
        videos = []
        for item in response.get('items', []):
            video_id = item['id']['videoId']

            # Get detailed statistics
            stats_response = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()

            stats = stats_response['items'][0]['statistics']

            videos.append({
                'video_id': video_id,
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'published_at': item['snippet']['publishedAt'],
                'view_count': int(stats.get('viewCount', 0)),
                'like_count': int(stats.get('likeCount', 0)),
                'comment_count': int(stats.get('commentCount', 0)),
                'thumbnail_url': item['snippet']['thumbnails']['high']['url']
            })

        return videos

    def calculate_popularity_index(self, video: Dict[str, any]) -> float:
        """
        Calculate popularity index for a video using scipy.

        Formula: PI = log(views) * 0.4 + log(likes) * 0.3 +
                     log(comments) * 0.2 + recency_score * 0.1
        """
        import numpy as np
        from datetime import datetime

        views = max(video['view_count'], 1)
        likes = max(video['like_count'], 1)
        comments = max(video['comment_count'], 1)

        # Calculate recency score (0-1, with 1 being most recent)
        published_date = datetime.fromisoformat(
            video['published_at'].replace('Z', '+00:00')
        )
        days_old = (datetime.now(timezone.utc) - published_date).days
        recency_score = 1 / (1 + days_old / 30)  # Decay over 30 days

        # Weighted popularity index
        popularity = (
            np.log10(views) * 0.4 +
            np.log10(likes) * 0.3 +
            np.log10(comments) * 0.2 +
            recency_score * 0.1
        ) * 10  # Scale to 0-100 range

        return round(min(popularity, 100), 2)
```

---

## 🔐 Security & Authentication

### JWT Authentication Implementation

#### Token Generation
```python
# File: app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)

def decode_token(token: str) -> dict:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

#### Authentication Dependency
```python
# File: app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.models.database.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user.

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials

    # Decode token
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    # Get user from database
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

### Role-Based Access Control (RBAC)

#### Permission System
```python
# File: app/core/permissions.py
from enum import Enum
from typing import List
from fastapi import HTTPException, status

class Permission(str, Enum):
    """System permissions."""
    # Brand permissions
    CREATE_BRAND = "create:brand"
    READ_BRAND = "read:brand"
    UPDATE_BRAND = "update:brand"
    DELETE_BRAND = "delete:brand"

    # Campaign permissions
    CREATE_CAMPAIGN = "create:campaign"
    READ_CAMPAIGN = "read:campaign"
    UPDATE_CAMPAIGN = "update:campaign"
    DELETE_CAMPAIGN = "delete:campaign"

    # Report permissions
    CREATE_REPORT = "create:report"
    READ_REPORT = "read:report"
    EXPORT_REPORT = "export:report"

    # Admin permissions
    MANAGE_USERS = "manage:users"
    VIEW_ANALYTICS = "view:analytics"

class Role(str, Enum):
    """System roles."""
    ADMIN = "admin"
    MANAGER = "manager"
    VIEWER = "viewer"

# Role-Permission mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: [permission for permission in Permission],
    Role.MANAGER: [
        Permission.CREATE_BRAND,
        Permission.READ_BRAND,
        Permission.UPDATE_BRAND,
        Permission.CREATE_CAMPAIGN,
        Permission.READ_CAMPAIGN,
        Permission.UPDATE_CAMPAIGN,
        Permission.CREATE_REPORT,
        Permission.READ_REPORT,
        Permission.EXPORT_REPORT,
        Permission.VIEW_ANALYTICS,
    ],
    Role.VIEWER: [
        Permission.READ_BRAND,
        Permission.READ_CAMPAIGN,
        Permission.READ_REPORT,
    ]
}

def check_permission(user: User, required_permission: Permission):
    """
    Check if user has required permission.

    Raises:
        HTTPException: If user doesn't have permission
    """
    user_role = user.role.role_name
    allowed_permissions = ROLE_PERMISSIONS.get(user_role, [])

    if required_permission not in allowed_permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required: {required_permission}"
        )
```

#### Permission Dependency
```python
# File: app/api/dependencies.py
from app.core.permissions import Permission, check_permission

def require_permission(permission: Permission):
    """
    Dependency factory to require specific permission.

    Usage:
        @router.post("/brands")
        async def create_brand(
            user: User = Depends(get_current_user),
            _permission_check = Depends(require_permission(Permission.CREATE_BRAND))
        ):
            ...
    """
    def permission_checker(user: User = Depends(get_current_user)):
        check_permission(user, permission)
        return True

    return permission_checker

# Usage in endpoints
@router.post("/api/v1/brands")
async def create_brand(
    brand: BrandCreate,
    user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(Permission.CREATE_BRAND))
):
    """Create brand (requires CREATE_BRAND permission)."""
    pass

@router.delete("/api/v1/brands/{brand_id}")
async def delete_brand(
    brand_id: int,
    user: User = Depends(get_current_user),
    _: bool = Depends(require_permission(Permission.DELETE_BRAND))
):
    """Delete brand (requires DELETE_BRAND permission)."""
    pass
```

### Data Encryption

#### Sensitive Field Encryption
```python
# File: app/core/encryption.py
from cryptography.fernet import Fernet
from app.core.config import settings

# Initialize Fernet cipher
cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_field(data: str) -> str:
    """Encrypt sensitive field."""
    if not data:
        return data
    encrypted = cipher_suite.encrypt(data.encode())
    return encrypted.decode()

def decrypt_field(encrypted_data: str) -> str:
    """Decrypt sensitive field."""
    if not encrypted_data:
        return encrypted_data
    decrypted = cipher_suite.decrypt(encrypted_data.encode())
    return decrypted.decode()

# Usage in models
class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    contract_name = Column(String(200))
    _sensitive_clause = Column("sensitive_clause", Text)  # Encrypted field

    @property
    def sensitive_clause(self) -> str:
        """Decrypt on read."""
        return decrypt_field(self._sensitive_clause)

    @sensitive_clause.setter
    def sensitive_clause(self, value: str):
        """Encrypt on write."""
        self._sensitive_clause = encrypt_field(value)
```

---

## 🧪 Testing Strategy

### Test Coverage Requirements

- **Unit Tests**: ≥80% coverage
- **Integration Tests**: All API endpoints
- **E2E Tests**: Critical user workflows

### Unit Testing Examples

```python
# File: tests/unit/services/test_brand_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.brand_service import BrandService
from app.models.schemas.brand import BrandCreate

@pytest.fixture
def mock_brand_repo():
    """Mock brand repository."""
    repo = MagicMock()
    repo.get_by_user = AsyncMock(return_value=[])
    repo.create = AsyncMock(return_value=MagicMock(id=1, brand_name="Test Brand"))
    return repo

@pytest.mark.asyncio
async def test_create_brand_success(mock_brand_repo):
    """Test successful brand creation."""
    service = BrandService(mock_brand_repo)
    brand_data = BrandCreate(
        brand_name="Test Brand",
        category="Beauty",
        slogan="Test Slogan"
    )

    result = await service.create_brand(brand_data, user_id=1)

    assert result.id == 1
    assert result.brand_name == "Test Brand"
    mock_brand_repo.create.assert_called_once()

@pytest.mark.asyncio
async def test_create_brand_exceeds_limit(mock_brand_repo):
    """Test brand creation when limit exceeded."""
    # Mock user already has MAX brands
    mock_brand_repo.get_by_user = AsyncMock(
        return_value=[MagicMock() for _ in range(100)]
    )

    service = BrandService(mock_brand_repo)
    brand_data = BrandCreate(brand_name="Test", category="Beauty")

    with pytest.raises(BusinessException, match="Maximum brand limit"):
        await service.create_brand(brand_data, user_id=1)
```

### Integration Testing Examples

```python
# File: tests/integration/test_brand_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from tests.utils import override_get_db, create_test_user

client = TestClient(app)

@pytest.fixture
def auth_headers():
    """Get authentication headers for test user."""
    user = create_test_user()
    token = create_access_token({"sub": user.id})
    return {"Authorization": f"Bearer {token}"}

def test_list_brands_empty(auth_headers):
    """Test listing brands when user has none."""
    response = client.get("/api/v1/brands", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert len(response.json()["data"]) == 0

def test_create_brand_success(auth_headers):
    """Test successful brand creation."""
    brand_data = {
        "brand_name": "Integration Test Brand",
        "category": "Technology",
        "slogan": "Test Slogan"
    }

    response = client.post(
        "/api/v1/brands",
        json=brand_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["brand_name"] == "Integration Test Brand"
    assert "id" in json_data["data"]

def test_create_brand_unauthorized():
    """Test brand creation without authentication."""
    brand_data = {
        "brand_name": "Test Brand",
        "category": "Technology"
    }

    response = client.post("/api/v1/brands", json=brand_data)
    assert response.status_code == 401
```

### End-to-End Testing Examples

```python
# File: tests/e2e/test_brand_workflow.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.e2e
def test_complete_brand_workflow():
    """
    Test complete brand workflow:
    1. User registration
    2. Login
    3. Create brand
    4. Get brand details
    5. Update brand
    6. Delete brand
    """
    # 1. Register user
    register_data = {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "name": "Test User"
    }
    response = client.post("/api/v1/auth/register", json=register_data)
    assert response.status_code == 201

    # 2. Login
    login_data = {
        "email": "test@example.com",
        "password": "SecurePass123!"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    token = response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create brand
    brand_data = {
        "brand_name": "E2E Test Brand",
        "category": "Beauty",
        "slogan": "Quality First"
    }
    response = client.post("/api/v1/brands", json=brand_data, headers=headers)
    assert response.status_code == 201
    brand_id = response.json()["data"]["id"]

    # 4. Get brand details
    response = client.get(f"/api/v1/brands/{brand_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["brand_name"] == "E2E Test Brand"

    # 5. Update brand
    update_data = {"slogan": "Updated Slogan"}
    response = client.put(
        f"/api/v1/brands/{brand_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["data"]["slogan"] == "Updated Slogan"

    # 6. Delete brand
    response = client.delete(f"/api/v1/brands/{brand_id}", headers=headers)
    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/api/v1/brands/{brand_id}", headers=headers)
    assert response.status_code == 404
```

---

## 🚀 Deployment Guide

### Docker Configuration

#### Production Dockerfile
```dockerfile
# Multi-stage build for optimized image size
FROM python:3.11.9-slim-bookworm AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip==24.3.1 && \
    pip install -r requirements.txt

# Final stage
FROM python:3.11.9-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### docker-compose.yml (Development)
```yaml
version: '3.8'

services:
  # FastAPI Backend
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: artnex-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://artnex_user:artnex_pass@db:5432/artnex_db
      - REDIS_URL=redis://redis:6379/0
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - IDEOGRAM_API_KEY=${IDEOGRAM_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=development
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./app:/app/app
      - ./logs:/app/logs
    networks:
      - artnex-network
    restart: unless-stopped

  # PostgreSQL Database
  db:
    image: postgres:15.8-bookworm
    container_name: artnex-db
    environment:
      POSTGRES_USER: artnex_user
      POSTGRES_PASSWORD: artnex_pass
      POSTGRES_DB: artnex_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init-db:/docker-entrypoint-initdb.d
    networks:
      - artnex-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U artnex_user -d artnex_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7.4.1-bookworm
    container_name: artnex-redis
    command: redis-server --appendonly yes --requirepass redis_pass
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data
    networks:
      - artnex-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:1.27.2-bookworm
    container_name: artnex-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./static:/var/www/static:ro
    depends_on:
      - backend
    networks:
      - artnex-network
    restart: unless-stopped

  # Celery Worker (Background tasks)
  celery-worker:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: artnex-celery-worker
    command: celery -A app.celery_app worker --loglevel=info --concurrency=4
    environment:
      - DATABASE_URL=postgresql://artnex_user:artnex_pass@db:5432/artnex_db
      - REDIS_URL=redis://:redis_pass@redis:6379/0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - IDEOGRAM_API_KEY=${IDEOGRAM_API_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app/app
      - ./logs:/app/logs
    networks:
      - artnex-network
    restart: unless-stopped

  # Flower (Celery monitoring)
  flower:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: artnex-flower
    command: celery -A app.celery_app flower --port=5555
    ports:
      - "5555:5555"
    environment:
      - REDIS_URL=redis://:redis_pass@redis:6379/0
    depends_on:
      - redis
      - celery-worker
    networks:
      - artnex-network
    restart: unless-stopped

volumes:
  pgdata:
    driver: local
  redisdata:
    driver: local

networks:
  artnex-network:
    driver: bridge
```

### AWS Deployment

#### EC2 Setup
```bash
# 1. Connect to EC2 instance
ssh -i "artnex-key.pem" ubuntu@ec2-xx-xx-xx-xx.ap-northeast-2.compute.amazonaws.com

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# 3. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Clone repository
git clone https://github.com/your-org/artnex.git
cd artnex

# 5. Configure environment
cp .env.example .env
vim .env  # Edit with production values

# 6. Deploy with Docker Compose
docker-compose up -d

# 7. Run database migrations
docker-compose exec backend alembic upgrade head

# 8. Check status
docker-compose ps
docker-compose logs -f backend
```

### Environment Variables (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis
REDIS_URL=redis://:password@host:6379/0

# AWS
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=artnex-mvp-files
AWS_REGION=ap-northeast-2

# AI APIs
OPENAI_API_KEY=sk-your-openai-key
IDEOGRAM_API_KEY=your-ideogram-key
YOUTUBE_API_KEY=your-youtube-key

# Security
SECRET_KEY=your-super-secret-key-min-32-chars
ENCRYPTION_KEY=your-encryption-key-base64

# Application
ENVIRONMENT=production
DEBUG=false
ALLOWED_ORIGINS=https://artnex.com,https://www.artnex.com

# Logging
LOG_LEVEL=INFO
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

---

## 👥 Team Structure & Responsibilities

### Backend Development Team (3 Developers)

#### Back1: Brand Management & Content Tracking
**Primary Responsibilities:**
- Main Dashboard API integration
- Brand Managing module (CRUD, KPI calculation, project/contract management)
- Content Tracking (SNS crawling API integration)

**Core Tables:**
- `Brands`, `Brand_KPIs`, `SKU`, `Projects`, `Contracts`, `Tracked_Contents`

**Key APIs:**
- SNS API (YouTube, TikTok) crawling
- S3 file upload/download
- Redis caching (dashboard data)

**Development Schedule (Summary):**
- **Week 1**: Main Dashboard API integration
- **Week 2-3**: Brand list data queries, KPI auto-calculation, Content Tracking
- **Week 4-5**: Brand registration form, Project management API
- **Week 6**: Contract management file storage API
- **Week 7**: Module integration and code review

#### Back2: Brand Insights & Reports
**Primary Responsibilities:**
- Brand Insight (GPT-based market analysis, keyword clustering)
- Brand Report (5-step diagnosis, AI analysis, PDF Export)
- ADMIN RBAC API (access control and role management)

**Core Tables:**
- `Brand_Insights`, `Insight_Results`, `Brand_Reports`, `Brand_Diagnostics`, `Report_Sections`

**Key Technologies:**
- GPT API prompt engineering
- scipy-based keyword clustering
- ReportLab-based PDF generation (multilingual support)

**Development Schedule (Summary):**
- **Week 1-2**: Brand Insight GPT integration
- **Week 3**: Brand list diagnosis API
- **Week 4**: Data input 5-step form
- **Week 5-6**: Brand diagnosis survey, Report view, ADMIN RBAC
- **Week 7**: Report Export API

#### Back3: Design/Shortform Studio & Campaigns
**Primary Responsibilities:**
- Design Studio (Ideogram API integration, tone & manner based design)
- Shortform Studio (text analysis, automatic storyboard generation)
- Campaign Manager (budget recommendations, influencer recommendations)
- Campaign Report (performance prediction AI, data visualization)

**Core Tables:**
- `Design_Projects`, `Shortform_Projects`, `Storyboard_Frames`, `Campaigns`, `Campaign_Reports`

**Key Technologies:**
- Ideogram API image generation
- Text analysis (cut segmentation algorithm)
- Performance prediction algorithm (scipy-based)

**Development Schedule (Summary):**
- **Week 1-2**: Design Studio Ideogram API
- **Week 3-4**: Shortform Studio, Campaign Manager
- **Week 5-7**: Campaign Report performance prediction AI, module integration

### Daily Collaboration

#### Communication Channels
- **Daily Standup**: 10:00 AM (15 minutes)
- **Code Review**: Pull Request reviews within 24 hours
- **Weekly Sync**: Friday 16:00 (Sprint review & retrospective)
- **Slack/Discord**: Real-time communication
- **GitHub Issues**: Task tracking and bug reporting

#### Shared Responsibilities (All Developers)
- Write unit tests for all new code (≥80% coverage)
- Document API endpoints in OpenAPI/Swagger
- Follow Python coding standards (PEP 8)
- Participate in code reviews
- Update project documentation
- Attend weekly team meetings

---

## 📚 Reference Documents

### Internal Documentation
1. **PRD**: `/prd/[수고랩]PRD_20251021_v1.0.pdf`
2. **Feature Specification**: `/prd/[수고랩]기능명세서_20251021_v1.0.pdf`
3. **Development Specification**: `/prd/[수고랩]개발명세서_20251021_v1.0.pdf`
4. **ERD**: `/prd/[수고랩]ERD_20251021_v1.0.pdf`
5. **WBS**: `/prd/[수고랩]아트넥스_WBS.pdf`

### Backend Development Schedules
1. **Back1**: `/prd/be-01/artnex_prd_day_be01.md`
2. **Back2**: `/prd/be-02/artnex_prd_day_be02.md`
3. **Back3**: `/prd/be-03/artnex_prd_day_be03.md`

### External API Documentation
1. **GPT API**: https://platform.openai.com/docs
2. **Ideogram API**: https://ideogram.ai/api/docs
3. **YouTube Data API**: https://developers.google.com/youtube/v3
4. **TikTok API**: https://developers.tiktok.com

---

## 🎯 Success Criteria

### Business KPIs
- User retention rate: ≥70%
- Monthly Active Users (MAU): 1,000 users
- Brand registration time: ≤5 minutes
- Report generation time: ≤5 minutes

### Technical KPIs
- AI response time: ≤5 seconds
- Page load time: ≤2 seconds
- API response time: ≤200ms (average)
- Test coverage: ≥80%
- System uptime: ≥99.5%

### Quality Metrics
- Zero critical security vulnerabilities
- Code review approval required for all PRs
- All API endpoints documented in Swagger
- Database queries use proper indexing
- Error logging with Sentry integration

---

## 📝 Document Metadata

**Document Version**: 2.0
**Created**: 2025-10-23
**Last Updated**: 2025-10-23
**Author**: Claude Code AI
**Status**: Active
**Project Version**: MVP 1.0

### Change History
#### v2.0 (2025-10-23)
- Complete restructure based on 8 source documents (5 PDFs + 3 MDs)
- Added hierarchical categorization (Tech Stack, Development Rules, Workflow, Critical Points)
- Comprehensive backend development guide with code examples
- Detailed security and authentication sections
- Enhanced testing strategy with examples
- Added deployment guide with Docker configurations
- Team structure and responsibilities clearly defined

#### v1.0 (2025-10-22)
- Initial document creation
- Basic project overview and goals
- Tech stack listing
- Development timeline

---

**© 2025 ArtNex Platform. All rights reserved.**
