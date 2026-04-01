from __future__ import annotations

from typing import Any
from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.parent.models import ParentProfile


# Repository for the ParentProfile model
# This repository is responsible for the database operations for the ParentProfile model
# It is used to get, create, update, and delete parent profiles from the database
# It is also responsible for the soft delete of the parent profiles
# It is also responsible for the recovery of the parent profiles
# It is also responsible for the hard delete of the parent profiles
# It is also responsible for the recovery of the parent profiles
class ParentRepository:
    async def get_by_user_id(
        self,
        db: AsyncSession,
        user_id: UUID,
    ) -> ParentProfile | None:
        stmt = select(ParentProfile).where(
            ParentProfile.user_id == user_id,
            ParentProfile.deleted_at.is_(None),
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        db: AsyncSession,
        parent_id: UUID,
    ) -> ParentProfile | None:
        stmt = select(ParentProfile).where(
            ParentProfile.id == parent_id,
            ParentProfile.deleted_at.is_(None),
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        db: AsyncSession,
        data: dict[str, Any],
    ) -> ParentProfile:
        parent = ParentProfile(**data)
        db.add(parent)
        await db.flush()
        await db.refresh(parent)
        return parent

    async def update(
        self,
        db: AsyncSession,
        parent: ParentProfile,
        data: dict[str, Any],
    ) -> ParentProfile:
        for field, value in data.items():
            setattr(parent, field, value)

        await db.flush()
        await db.refresh(parent)
        return parent
    
    async def soft_delete(
        self,
        db: AsyncSession,
        parent: ParentProfile,
    ) -> ParentProfile:
        parent.deleted_at = datetime.now(UTC)
        parent.is_active = False
        await db.flush()
        await db.refresh(parent)
        return parent