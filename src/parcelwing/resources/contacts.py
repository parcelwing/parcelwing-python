"""Contacts resource."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence, Union
from urllib.parse import quote

from .._http import HttpClient


class ContactsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, **params: Any) -> Dict[str, Any]:
        return dict(self._http.request("GET", "/api/contacts", params=params))

    def create(
        self, contact: Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        body: Any
        if isinstance(contact, Mapping):
            body = dict(contact)
        else:
            body = [dict(item) for item in contact]

        response = self._http.request("POST", "/api/contacts", json_body=body)
        return response.get("data")

    def get(self, contact_id: str) -> Dict[str, Any]:
        response = self._http.request(
            "GET", f"/api/contacts/{quote(contact_id, safe='')}"
        )
        return dict(response.get("data", {}))

    def update(self, contact_id: str, contact: Mapping[str, Any]) -> Dict[str, Any]:
        response = self._http.request(
            "PATCH",
            f"/api/contacts/{quote(contact_id, safe='')}",
            json_body=dict(contact),
        )
        return dict(response.get("data", {}))

    def delete(self, contact_id: str) -> Dict[str, Any]:
        return dict(
            self._http.request("DELETE", f"/api/contacts/{quote(contact_id, safe='')}")
        )
