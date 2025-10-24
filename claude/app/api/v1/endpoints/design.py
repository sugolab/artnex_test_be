"""
Design Studio API Endpoints (Back3)
디자인 스튜디오 Ideogram API 연동
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.design import DesignProject
from app.schemas.design import DesignProjectCreate, DesignProjectResponse

router = APIRouter()


@router.post("/design-projects", response_model=DesignProjectResponse, status_code=201)
async def create_design_project(
    project_data: DesignProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    디자인 프로젝트 생성 (Back3 Day 1 작업)

    - Design_Projects 테이블 생성
    - 톤앤매너 입력 파싱
    """
    project = DesignProject(
        brand_id=project_data.brand_id,
        user_id=current_user.id,
        project_name=project_data.project_name,
        input_type=project_data.input_type,
        tone_manner=project_data.tone_manner,
        color_palette=project_data.color_palette,
        prompt=project_data.prompt,
        keywords=project_data.keywords,
        bid_report_id=project_data.bid_report_id
    )

    db.add(project)
    await db.commit()
    await db.refresh(project)

    return project


@router.get("/design-projects", response_model=list[DesignProjectResponse])
async def list_design_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """디자인 프로젝트 목록 조회"""
    result = await db.execute(
        select(DesignProject).where(DesignProject.user_id == current_user.id)
    )
    projects = result.scalars().all()
    return projects


@router.get("/design-projects/{project_id}", response_model=DesignProjectResponse)
async def get_design_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """디자인 프로젝트 상세 조회"""
    project = await db.get(DesignProject, project_id)

    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다")

    return project
