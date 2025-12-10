class DomainError(Exception):
    code = None
    """Base class for business-level errors."""


class NotFoundError(DomainError):
    def __init__(self, message: str = "Resource not found"):
        self.code = "not_found"
        self.message = message
        super().__init__(message)


class PermissionDenied(DomainError):
    def __init__(self, message: str = "Permission denied"):
        self.code = "permission_denied"
        self.message = message
        super().__init__(message)
