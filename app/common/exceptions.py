from fastapi import Request
from fastapi.responses import JSONResponse


class DomainError(Exception):
    code = None
    """Base class for business-level errors."""


class NotFoundError(DomainError):
    def __init__(self, message: str = "Resource not found"):
        self.code = "not_found"
        self.message = message
        super().__init__(message)


async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


class PermissionDenied(DomainError):
    def __init__(self, message: str = "Permission denied"):
        self.code = "permission_denied"
        self.message = message
        super().__init__(message)


async def permission_handler(request: Request, exc: PermissionDenied):
    return JSONResponse(
        status_code=403,
        content={"detail": exc.message},
    )
