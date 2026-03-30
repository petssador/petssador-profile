from app.core.exceptions import ConflictError, NotFoundError, ValidationError


class ParentAlreadyExistsError(ConflictError):
    pass


class ParentNotFoundError(NotFoundError):
    pass


class ParentOnboardingValidationError(ValidationError):
    pass


class ParentInactiveError(ValidationError):
    pass