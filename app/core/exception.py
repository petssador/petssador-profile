class AppException(Exception):
    """Base application exception."""


class NotFoundError(AppException):
    """Raised when a resource is not found."""


class ConflictError(AppException):
    """Raised when a resource already exists."""


class ValidationError(AppException):
    """Raised when business validation fails."""