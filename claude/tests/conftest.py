"""
Pytest Configuration and Fixtures
테스트를 위한 공통 설정 및 픽스처
"""
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings
from app.models.user import User, Role
from app.models.brand import Brand
from app.core.security import get_password_hash


# Test database URL (SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """
    테스트용 데이터베이스 세션 생성
    각 테스트 함수마다 새로운 데이터베이스를 생성하고 종료 시 삭제
    """
    # Create test engine
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    테스트용 HTTP 클라이언트
    """
    async def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_db: AsyncSession) -> User:
    """
    테스트용 사용자 생성
    """
    # Create role first
    role = Role(role_name="user", description="Regular user")
    test_db.add(role)
    await test_db.commit()
    await test_db.refresh(role)

    # Create user
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("password123"),
        name="Test User",
        role_id=role.id,
        is_active=True,
        is_verified=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)

    return user


@pytest.fixture
async def test_brand(test_db: AsyncSession, test_user: User) -> Brand:
    """
    테스트용 브랜드 생성
    """
    brand = Brand(
        user_id=test_user.id,
        brand_name="Test Brand",
        category="뷰티",
        industry="화장품",
        slogan="Test Slogan",
        keywords=["뷰티", "화장품", "스킨케어"]
    )
    test_db.add(brand)
    await test_db.commit()
    await test_db.refresh(brand)

    return brand


@pytest.fixture
async def auth_headers(client: AsyncClient, test_user: User) -> dict:
    """
    인증 헤더 생성 (JWT 토큰)
    """
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
