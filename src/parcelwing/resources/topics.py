"""Topics resource."""

from __future__ import annotations

from typing import Any, Dict, Mapping
from urllib.parse import quote

from .._http import HttpClient


class TopicsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, **params: Any) -> Dict[str, Any]:
        return dict(self._http.request("GET", "/api/topics", params=params))

    def create(self, topic: Mapping[str, Any]) -> Dict[str, Any]:
        response = self._http.request("POST", "/api/topics", json_body=dict(topic))
        return dict(response.get("data", {}))

    def get(self, topic_id: str) -> Dict[str, Any]:
        response = self._http.request("GET", f"/api/topics/{quote(topic_id, safe='')}")
        return dict(response.get("data", {}))

    def update(self, topic_id: str, topic: Mapping[str, Any]) -> Dict[str, Any]:
        response = self._http.request(
            "PATCH",
            f"/api/topics/{quote(topic_id, safe='')}",
            json_body=dict(topic),
        )
        return dict(response.get("data", {}))

    def delete(self, topic_id: str) -> Dict[str, Any]:
        return dict(
            self._http.request("DELETE", f"/api/topics/{quote(topic_id, safe='')}")
        )
