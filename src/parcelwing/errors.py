"""Parcel Wing SDK exceptions."""

from __future__ import annotations

from typing import Any, Dict, Literal, Optional

ParcelWingErrorType = Literal[
    "authentication_error",
    "validation_error",
    "invalid_request_error",
    "not_found_error",
    "conflict_error",
    "rate_limit_error",
    "reputation_error",
    "suppression_error",
    "api_error",
]


class ParcelWingError(Exception):
    """Raised when a Parcel Wing API request fails."""

    def __init__(
        self,
        message: str,
        *,
        status: int,
        type: ParcelWingErrorType = "api_error",
        code: Optional[str] = None,
        request_id: Optional[str] = None,
        details: Any = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.type = type
        self.code = code
        self.request_id = request_id
        self.details = details
        self.metadata = metadata or {}

    def __repr__(self) -> str:
        return (
            "ParcelWingError("
            f"status={self.status!r}, type={self.type!r}, "
            f"code={self.code!r}, message={self.message!r})"
        )


def is_parcelwing_error(error: BaseException) -> bool:
    """Return True when *error* is a ParcelWingError."""

    return isinstance(error, ParcelWingError)
