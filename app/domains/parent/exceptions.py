from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError, ValidationError


class ParentAlreadyExistsError(ConflictError):
    pass


class ParentNotFoundError(NotFoundError):
    pass


class ParentOnboardingValidationError(ValidationError):
    pass


class ParentInactiveError(ValidationError):
    pass


class ParentInactiveError(ForbiddenError):
    pass