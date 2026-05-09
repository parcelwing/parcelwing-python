"""Segments resource."""

from __future__ import annotations

from typing import Any, Dict, Mapping
from urllib.parse import quote

from .._http import HttpClient


class SegmentsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, **params: Any) -> Dict[str, Any]:
        return dict(self._http.request("GET", "/api/segments", params=params))

    def create(self, segment: Mapping[str, Any]) -> Dict[str, Any]:
        response = self._http.request("POST", "/api/segments", json_body=dict(segment))
        return dict(response.get("data", {}))

    def get(self, segment_id: str) -> Dict[str, Any]:
        response = self._http.request(
            "GET", f"/api/segments/{quote(segment_id, safe='')}"
        )
        return dict(response.get("data", {}))

    def update(self, segment_id: str, segment: Mapping[str, Any]) -> Dict[str, Any]:
        response = self._http.request(
            "PATCH",
            f"/api/segments/{quote(segment_id, safe='')}",
            json_body=dict(segment),
        )
        return dict(response.get("data", {}))

    def delete(self, segment_id: str) -> Dict[str, Any]:
        return dict(
            self._http.request("DELETE", f"/api/segments/{quote(segment_id, safe='')}")
        )
