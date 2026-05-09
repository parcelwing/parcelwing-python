"""Internal HTTP transport for the Parcel Wing SDK."""

from __future__ import annotations

import json
from typing import Any, Dict, Mapping, Optional
from urllib.parse import urlencode

import httpx

from .errors import ParcelWingError, ParcelWingErrorType

SDK_VERSION = "0.1.0"
DEFAULT_BASE_URL = "https://parcelwing.com"


class HttpClient:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        headers: Optional[Mapping[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("ParcelWing client requires a non-empty api_key.")

        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = dict(headers or {})
        self._client = http_client
        self._owns_client = http_client is None

        if self._client is None:
            self._client = httpx.Client(timeout=timeout)

    def close(self) -> None:
        if self._owns_client and self._client is not None:
            self._client.close()

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Any = None,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        if self._client is None:
            raise RuntimeError("Parcel Wing HTTP client is closed.")

        url = f"{self.base_url}{path}"
        if params:
            query = to_query_string(params)
            if query:
                url = f"{url}?{query}"

        request_headers: Dict[str, str] = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-ParcelWing-SDK": f"python/{SDK_VERSION}",
            **self.headers,
            **dict(headers or {}),
        }
        if json_body is not None:
            request_headers["Content-Type"] = "application/json"

        try:
            response = self._client.request(
                method,
                url,
                headers=request_headers,
                json=json_body,
                timeout=self.timeout,
            )
        except httpx.TimeoutException as exc:
            raise ParcelWingError(
                f"Request timed out after {self.timeout}s.",
                status=408,
                type="api_error",
                code="request_timeout",
            ) from exc
        except httpx.HTTPError as exc:
            raise ParcelWingError(
                str(exc),
                status=0,
                type="api_error",
                code="network_error",
            ) from exc

        text = response.text
        parsed = _safe_json_parse(text)

        if response.status_code < 200 or response.status_code >= 300:
            raise _to_parcelwing_error(response.status_code, parsed, text)

        return parsed


def to_query_string(params: Mapping[str, Any]) -> str:
    clean: Dict[str, str] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            clean[key] = "true" if value else "false"
        else:
            clean[key] = str(value)
    return urlencode(clean)


def unwrap_resource(response: Mapping[str, Any]) -> Any:
    return response.get("data")


def _safe_json_parse(value: str) -> Any:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def _to_parcelwing_error(status: int, parsed: Any, fallback_text: str) -> ParcelWingError:
    if isinstance(parsed, Mapping) and isinstance(parsed.get("error"), Mapping):
        error = parsed["error"]
        message = str(error.get("message") or fallback_text or "Parcel Wing API error.")
        error_type = str(error.get("type") or "api_error")
        allowed_types = {
            "authentication_error",
            "validation_error",
            "invalid_request_error",
            "not_found_error",
            "conflict_error",
            "rate_limit_error",
            "reputation_error",
            "suppression_error",
            "api_error",
        }
        if error_type not in allowed_types:
            error_type = "api_error"

        metadata = {
            str(key): value
            for key, value in error.items()
            if key not in {"type", "code", "message", "details", "request_id"}
        }
        return ParcelWingError(
            message,
            status=status,
            type=error_type,  # type: ignore[arg-type]
            code=error.get("code") if isinstance(error.get("code"), str) else None,
            request_id=error.get("request_id")
            if isinstance(error.get("request_id"), str)
            else None,
            details=error.get("details"),
            metadata=metadata,
        )

    return ParcelWingError(
        fallback_text or f"Parcel Wing API request failed with status {status}.",
        status=status,
        type="api_error",
        code="http_error",
    )
