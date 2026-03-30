from app.core.exceptions import ConflictError, NotFoundError, ValidationError


class ProviderAlreadyExistsError(ConflictError):
    pass


class ProviderNotFoundError(NotFoundError):
    pass


class ProviderValidationError(ValidationError):
    pass