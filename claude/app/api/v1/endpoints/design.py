"""
Design Studio API Endpoints (Back3)
디자인 스튜디오 Ideogram API 연동
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.design import DesignProject, DesignResult
from app.models.brand import Brand
from app.schemas.design import DesignProjectCreate, DesignProjectResponse, IdeogramGenerateRequest
from app.services.ideogram_service import IdeogramService

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


@router.post("/design-projects/{project_id}/generate")
async def generate_design_images(
    project_id: int,
    custom_prompt: str = None,
    style: str = "design",
    num_images: int = 4,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ideogram API를 사용하여 디자인 이미지 생성 (Back3 Day 2)

    - 브랜드 정보 기반 자동 프롬프트 생성
    - 톤앤매너 및 컬러 팔레트 적용
    - Ideogram API 호출 및 결과 저장
    """
    # 프로젝트 조회
    project = await db.get(DesignProject, project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다")

    # 브랜드 정보 조회
    brand = await db.get(Brand, project.brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="브랜드를 찾을 수 없습니다")

    # Ideogram Service 초기화
    ideogram_service = IdeogramService()

    # 커스텀 프롬프트가 없으면 자동 생성
    if custom_prompt:
        final_prompt = custom_prompt
    else:
        final_prompt = ideogram_service.build_design_prompt(
            brand_name=brand.brand_name,
            industry=brand.industry or "general",
            tone_manner=project.tone_manner,
            keywords=project.keywords
        )

    # 이미지 생성
    result = await ideogram_service.generate_image(
        prompt=final_prompt,
        style=style,
        aspect_ratio="1:1",
        num_images=num_images,
        color_palette=project.color_palette
    )

    # 생성 성공 시 데이터베이스에 저장
    if result.get("success"):
        saved_results = []
        for image_data in result.get("images", []):
            design_result = DesignResult(
                project_id=project.id,
                image_url=image_data["url"],
                ideogram_id=image_data.get("image_id"),
                generation_prompt=final_prompt,
                style=style
            )
            db.add(design_result)
            saved_results.append(design_result)

        await db.commit()

        # 저장된 결과 반환
        return {
            "success": True,
            "message": "이미지 생성 완료",
            "project_id": project.id,
            "images": result.get("images", []),
            "prompt_used": final_prompt,
            "style": style,
            "mock": result.get("mock", False)
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"이미지 생성 실패: {result.get('error', 'Unknown error')}"
        )


@router.post("/design-projects/{project_id}/regenerate")
async def regenerate_design_images(
    project_id: int,
    result_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    기존 디자인 결과 재생성 (Back3 Day 2)

    - 기존 프롬프트 사용하여 새로운 이미지 생성
    """
    # 프로젝트 확인
    project = await db.get(DesignProject, project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다")

    # 기존 결과 조회
    existing_result = await db.get(DesignResult, result_id)
    if not existing_result or existing_result.project_id != project_id:
        raise HTTPException(status_code=404, detail="디자인 결과를 찾을 수 없습니다")

    # Ideogram Service로 재생성
    ideogram_service = IdeogramService()
    result = await ideogram_service.generate_image(
        prompt=existing_result.generation_prompt,
        style=existing_result.style or "design",
        aspect_ratio="1:1",
        num_images=1,
        color_palette=project.color_palette
    )

    if result.get("success") and result.get("images"):
        # 새로운 결과로 업데이트
        image_data = result["images"][0]
        existing_result.image_url = image_data["url"]
        existing_result.ideogram_id = image_data.get("image_id")

        await db.commit()
        await db.refresh(existing_result)

        return {
            "success": True,
            "message": "이미지 재생성 완료",
            "result": existing_result,
            "mock": result.get("mock", False)
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"이미지 재생성 실패: {result.get('error', 'Unknown error')}"
        )
