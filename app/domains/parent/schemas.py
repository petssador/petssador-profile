from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ParentBase(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone_number: str | None = Field(default=None, max_length=30)
    alternate_phone: str | None = Field(default=None, max_length=30)

    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    profile_image_url: str | None = None

    country: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    address_line_1: str | None = Field(default=None, max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=30)

    emergency_name: str | None = Field(default=None, max_length=150)
    emergency_phone: str | None = Field(default=None, max_length=30)
    emergency_relation: str | None = Field(default=None, max_length=80)

    preferred_contact_method: str | None = Field(default=None, max_length=30)
    marketing_opt_in: bool | None = None


class ParentCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone_number: str | None = Field(default=None, max_length=30)


class ParentUpdate(ParentBase):
    pass


class ParentOnboardingUpdate(BaseModel):
    onboarding_step: int = Field(..., ge=0)

    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone_number: str | None = Field(default=None, max_length=30)

    country: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    address_line_1: str | None = Field(default=None, max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=30)

    emergency_name: str | None = Field(default=None, max_length=150)
    emergency_phone: str | None = Field(default=None, max_length=30)
    emergency_relation: str | None = Field(default=None, max_length=80)

    preferred_contact_method: str | None = Field(default=None, max_length=30)
    marketing_opt_in: bool | None = None


class ParentOnboardingCompleteResponse(BaseModel):
    message: str
    onboarding_step: int
    onboarding_completed: bool


class ParentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID

    first_name: str
    last_name: str
    phone_number: str | None
    alternate_phone: str | None

    date_of_birth: date | None
    gender: str | None
    profile_image_url: str | None

    country: str | None
    state: str | None
    city: str | None
    address_line_1: str | None
    address_line_2: str | None
    postal_code: str | None

    emergency_name: str | None
    emergency_phone: str | None
    emergency_relation: str | None

    preferred_contact_method: str | None
    marketing_opt_in: bool

    onboarding_step: int
    onboarding_completed: bool
    is_active: bool

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None