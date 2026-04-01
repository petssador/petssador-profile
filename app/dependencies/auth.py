from dataclasses import dataclass
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status


@dataclass
class CurrentUser:
    id: UUID
    email: str


async def get_current_user() -> CurrentUser:
    """
    Replace this with your real authenticated user dependency.
    """
    return CurrentUser(
        id=uuid4(),
        email="test@petssador.com",
    )