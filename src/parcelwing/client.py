"""Parcel Wing API client."""

from __future__ import annotations

from typing import Mapping, Optional

import httpx

from ._http import DEFAULT_BASE_URL, HttpClient
from .resources import (
    AutomationsResource,
    ContactsResource,
    EmailsResource,
    SegmentsResource,
    TopicsResource,
)


class ParcelWing:
    """Client for the Parcel Wing API."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        headers: Optional[Mapping[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self.http = HttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            headers=headers,
            http_client=http_client,
        )
        self.emails = EmailsResource(self.http)
        self.contacts = ContactsResource(self.http)
        self.segments = SegmentsResource(self.http)
        self.topics = TopicsResource(self.http)
        self.automations = AutomationsResource(self.http)

    def close(self) -> None:
        self.http.close()

    def __enter__(self) -> "ParcelWing":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()
