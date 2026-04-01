from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.parent.exceptions import (
    ParentAlreadyExistsError,
    ParentInactiveError,
    ParentNotFoundError,
)
from app.domains.parent.models import ParentProfile
from app.domains.parent.repository import ParentRepository
from app.domains.parent.schemas import (
    ParentCreate,
    ParentOnboardingCompleteResponse,
    ParentOnboardingUpdate,
    ParentUpdate,
)
from app.domains.parent.validators import (
    validate_onboarding_step_transition,
    validate_parent_onboarding_completion,
)


# Service for the ParentProfile model
class ParentService:
    def __init__(self, repository: ParentRepository | None = None) -> None:
        self.repository = repository or ParentRepository()

    # Helper method to get the active parent for a user or raise an error if not found or inactive
    async def _get_active_parent_or_raise(
        self,
        db: AsyncSession,
        user_id: UUID,
    ) -> ParentProfile:
        parent = await self.repository.get_by_user_id(db, user_id)
        if not parent:
            raise ParentNotFoundError("Parent profile not found.")
        if not parent.is_active:
            raise ParentInactiveError("Parent profile is inactive.")
        return parent

    async def create_parent_for_user(
        self,
        db: AsyncSession,
        user_id: UUID,
        payload: ParentCreate,
    ) -> ParentProfile:
        existing = await self.repository.get_by_user_id(db, user_id)
        if existing:
            raise ParentAlreadyExistsError("Parent profile already exists for this user.")

        data = payload.model_dump()
        data["first_name"] = data["first_name"].strip()
        data["last_name"] = data["last_name"].strip()

        if data.get("phone_number"):
            data["phone_number"] = data["phone_number"].strip()

        data["user_id"] = user_id
        data["onboarding_step"] = 1
        data["onboarding_completed"] = False
        data["is_active"] = True

        try:
            parent = await self.repository.create(db, data)
            await db.commit()
            await db.refresh(parent)
            return parent
        except Exception:
            await db.rollback()
            raise

    async def get_parent_for_user(
        self,
        db: AsyncSession,
        user_id: UUID,
    ) -> ParentProfile:
        return await self._get_active_parent_or_raise(db, user_id)

    async def update_parent_for_user(
        self,
        db: AsyncSession,
        user_id: UUID,
        payload: ParentUpdate,
    ) -> ParentProfile:
        parent = await self._get_active_parent_or_raise(db, user_id)
        updates = payload.model_dump(exclude_unset=True)

        for key in ("first_name", "last_name", "phone_number", "alternate_phone"):
            if key in updates and updates[key] is not None:
                updates[key] = updates[key].strip()

        try:
            parent = await self.repository.update(db, parent, updates)
            await db.commit()
            await db.refresh(parent)
            return parent
        except Exception:
            await db.rollback()
            raise

    async def save_onboarding_progress(
        self,
        db: AsyncSession,
        user_id: UUID,
        payload: ParentOnboardingUpdate,
    ) -> ParentProfile:
        parent = await self._get_active_parent_or_raise(db, user_id)

        validate_onboarding_step_transition(
            current_step=parent.onboarding_step,
            new_step=payload.onboarding_step,
        )

        updates = payload.model_dump(exclude_unset=True)

        for key in ("first_name", "last_name", "phone_number", "emergency_phone"):
            if key in updates and updates[key] is not None:
                updates[key] = updates[key].strip()

        try:
            parent = await self.repository.update(db, parent, updates)
            await db.commit()
            await db.refresh(parent)
            return parent
        except Exception:
            await db.rollback()
            raise

    async def complete_onboarding(
        self,
        db: AsyncSession,
        user_id: UUID,
    ) -> ParentOnboardingCompleteResponse:
        parent = await self._get_active_parent_or_raise(db, user_id)

        validate_parent_onboarding_completion(parent)

        try:
            parent = await self.repository.update(
                db,
                parent,
                {
                    "onboarding_step": max(parent.onboarding_step, 5),
                    "onboarding_completed": True,
                },
            )
            await db.commit()
            await db.refresh(parent)

            return ParentOnboardingCompleteResponse(
                message="Parent onboarding completed successfully.",
                onboarding_step=parent.onboarding_step,
                onboarding_completed=parent.onboarding_completed,
            )
        except Exception:
            await db.rollback()
            raise