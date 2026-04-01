from app.domains.parent.exceptions import ParentOnboardingValidationError
from app.domains.parent.models import ParentProfile


REQUIRED_ONBOARDING_FIELDS = (
    "first_name",
    "last_name",
    "phone_number",
    "country",
    "state",
    "city",
)


def validate_onboarding_step_transition(current_step: int, new_step: int) -> None:
    if new_step < 0:
        raise ParentOnboardingValidationError("Onboarding step cannot be negative.")

    if new_step > current_step + 1:
        raise ParentOnboardingValidationError(
            f"Invalid onboarding step transition from {current_step} to {new_step}."
        )


def validate_parent_onboarding_completion(parent: ParentProfile) -> None:
    missing_fields = [
        field_name
        for field_name in REQUIRED_ONBOARDING_FIELDS
        if not getattr(parent, field_name, None)
    ]

    if missing_fields:
        raise ParentOnboardingValidationError(
            f"Cannot complete onboarding. Missing required fields: {', '.join(missing_fields)}."
        )