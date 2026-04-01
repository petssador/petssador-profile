from sqlalchemy import Column, Table
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

users = Table(
    "users",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    extend_existing=True,
)