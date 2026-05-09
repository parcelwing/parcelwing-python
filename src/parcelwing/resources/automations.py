"""Automation events resource."""

from __future__ import annotations

from typing import Any, Dict, Mapping

from .._http import HttpClient


class AutomationsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def track(self, event: Mapping[str, Any]) -> Dict[str, Any]:
        response = self._http.request(
            "POST", "/api/automations/events", json_body=dict(event)
        )
        return dict(response.get("data", {}))
