class AppException(Exception):
    def __init__(self, message: str = "Application error"):
        self.message = message
        super().__init__(message)


class NotFoundError(AppException):
    pass


class ConflictError(AppException):
    pass


class ValidationError(AppException):
    pass

class ForbiddenError(AppException):
    pass