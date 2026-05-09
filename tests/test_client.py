from __future__ import annotations

import json

import httpx
import pytest

from parcelwing import ParcelWing, ParcelWingError


def make_client(handler):
    transport = httpx.MockTransport(handler)
    http_client = httpx.Client(transport=transport)
    return ParcelWing(
        api_key="pw_test_123",
        base_url="https://example.parcelwing.test",
        http_client=http_client,
    )


def test_send_email_posts_to_api_emails():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert str(request.url) == "https://example.parcelwing.test/api/emails"
        assert request.headers["authorization"] == "Bearer pw_test_123"
        assert request.headers["x-parcelwing-sdk"] == "python/0.1.0"
        body = json.loads(request.content.decode())
        assert body == {
            "from": "Acme <hello@example.com>",
            "to": "person@example.com",
            "subject": "Hello",
            "text": "It works.",
        }
        return httpx.Response(
            202,
            json={
                "object": "list",
                "data": [
                    {"object": "email", "id": "msg_123", "to": "person@example.com", "status": "queued"}
                ],
            },
        )

    client = make_client(handler)
    result = client.emails.send(
        from_="Acme <hello@example.com>",
        to="person@example.com",
        subject="Hello",
        text="It works.",
    )

    assert result[0]["id"] == "msg_123"


def test_raw_email_dict_preserves_api_from_key():
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content.decode())
        assert body["from"] == "Acme <hello@example.com>"
        return httpx.Response(202, json={"object": "list", "data": []})

    client = make_client(handler)
    assert client.emails.send({"from": "Acme <hello@example.com>", "to": "a@example.com", "text": "Hi"}) == []


def test_list_query_params_encode_booleans():
    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == (
            "https://example.parcelwing.test/api/segments?active=true&include_counts=false&page=2"
        )
        return httpx.Response(200, json={"object": "list", "data": []})

    client = make_client(handler)
    client.segments.list(active=True, include_counts=False, page=2)


def test_resource_methods_unwrap_data():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "object": "contact",
                "data": {"object": "contact", "id": "contact_123", "email": "person@example.com"},
            },
        )

    client = make_client(handler)
    contact = client.contacts.get("contact_123")
    assert contact["email"] == "person@example.com"


def test_api_error_shape_maps_to_parcelwing_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            json={
                "error": {
                    "type": "validation_error",
                    "code": "invalid_request_body",
                    "message": "Invalid request body.",
                    "request_id": "req_123",
                    "details": {"fieldErrors": {}},
                }
            },
        )

    client = make_client(handler)

    with pytest.raises(ParcelWingError) as exc:
        client.emails.send(from_="bad", to="person@example.com", text="Hi")

    assert exc.value.status == 400
    assert exc.value.type == "validation_error"
    assert exc.value.code == "invalid_request_body"
    assert exc.value.request_id == "req_123"
    assert exc.value.details == {"fieldErrors": {}}


def test_requires_api_key():
    with pytest.raises(ValueError, match="api_key"):
        ParcelWing(api_key="")
