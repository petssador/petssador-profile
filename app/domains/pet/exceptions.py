from app.core.exceptions import ConflictError, NotFoundError, ValidationError


class PetAlreadyExistsError(ConflictError):
    pass


class PetNotFoundError(NotFoundError):
    pass


class PetValidationError(ValidationError):
    pass