"""Email sending resource."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from .._http import HttpClient

EmailRecipient = Union[str, Sequence[str]]


class EmailsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def send(
        self,
        email: Optional[Mapping[str, Any]] = None,
        *,
        from_: Optional[str] = None,
        to: Optional[EmailRecipient] = None,
        subject: Optional[str] = None,
        text: Optional[str] = None,
        html: Optional[str] = None,
        reply_to: Optional[str] = None,
        tags: Optional[Mapping[str, str]] = None,
        template_id: Optional[str] = None,
        template_alias: Optional[str] = None,
        template_params: Optional[Mapping[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Queue one email request.

        Pass either a raw request dict using API field names, or keyword arguments.
        Because ``from`` is a Python keyword, use ``from_`` with keyword arguments.
        """

        payload: Dict[str, Any]
        if email is not None:
            payload = dict(email)
        else:
            payload = {}

        if from_ is not None:
            payload["from"] = from_
        if to is not None:
            payload["to"] = list(to) if not isinstance(to, str) else to
        if subject is not None:
            payload["subject"] = subject
        if text is not None:
            payload["text"] = text
        if html is not None:
            payload["html"] = html
        if reply_to is not None:
            payload["reply_to"] = reply_to
        if tags is not None:
            payload["tags"] = dict(tags)
        if template_id is not None:
            payload["template_id"] = template_id
        if template_alias is not None:
            payload["template_alias"] = template_alias
        if template_params is not None:
            payload["template_params"] = dict(template_params)

        response = self._http.request("POST", "/api/emails", json_body=payload)
        return list(response.get("data", []))
