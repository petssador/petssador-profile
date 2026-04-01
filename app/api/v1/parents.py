from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import CurrentUser, get_current_user
from app.domains.parent.repository import ParentRepository
from app.domains.parent.schemas import (
    ParentCreate,
    ParentOnboardingCompleteResponse,
    ParentOnboardingUpdate,
    ParentResponse,
    ParentUpdate,
)
from app.domains.parent.service import ParentService

router = APIRouter()


# Dependency to get the parent service
def get_parent_service() -> ParentService:
    return ParentService(repository=ParentRepository())


@router.post(
    "/me",
    response_model=ParentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_my_parent_profile(
    payload: ParentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    service: ParentService = Depends(get_parent_service),
):
    return await service.create_parent_for_user(db, current_user.id, payload)


@router.get(
    "/me",
    response_model=ParentResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_parent_profile(
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    service: ParentService = Depends(get_parent_service),
):
    return await service.get_parent_for_user(db, current_user.id)


@router.patch(
    "/me",
    response_model=ParentResponse,
    status_code=status.HTTP_200_OK,
)
async def update_my_parent_profile(
    payload: ParentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    service: ParentService = Depends(get_parent_service),
):
    return await service.update_parent_for_user(db, current_user.id, payload)


@router.patch(
    "/me/onboarding",
    response_model=ParentResponse,
    status_code=status.HTTP_200_OK,
)
async def save_my_parent_onboarding_progress(
    payload: ParentOnboardingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    service: ParentService = Depends(get_parent_service),
):
    return await service.save_onboarding_progress(db, current_user.id, payload)


@router.post(
    "/me/onboarding/complete",
    response_model=ParentOnboardingCompleteResponse,
    status_code=status.HTTP_200_OK,
)
async def complete_my_parent_onboarding(
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    service: ParentService = Depends(get_parent_service),
):
    return await service.complete_onboarding(db, current_user.id)