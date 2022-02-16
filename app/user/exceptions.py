from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = "User not found",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)


class UserEmailAlreadyExistsException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        detail: Any = "User email already exists",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)


class UnauthorizedException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = "Unauthorized",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)


class ForbiddenException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        detail: Any = "Forbidden",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)
