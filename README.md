# Parcel Wing Python SDK

The official Python SDK for the Parcel Wing API.

It is designed for a fast, predictable developer experience:

- resource clients for emails, contacts, segments, topics, and automations
- consistent `ParcelWingError` exceptions
- typed package metadata and exported type hints
- small dependency surface built on `httpx`
- works with the same public API contract used by Parcel Wing itself

## Installation

```bash
pip install parcelwing
```

## Quick start

First you'll need an API key. If you don't have one, sign up and create one at https://parcelwing.com/signup. It's free, with no credit card required.

```python
import os

from parcelwing import ParcelWing

parcel_wing = ParcelWing(api_key=os.environ["PARCEL_WING_API_KEY"])

emails = parcel_wing.emails.send(
    from_="Acme <hello@yourdomain.com>",
    to="person@example.com",
    subject="Hello from Parcel Wing",
    text="It works.",
)

print(emails[0]["id"])
```

`from` is a Python keyword, so the keyword-argument API uses `from_`. You can also pass a raw API dictionary if you prefer exact API field names:

```python
emails = parcel_wing.emails.send({
    "from": "Acme <hello@yourdomain.com>",
    "to": "person@example.com",
    "subject": "Hello from Parcel Wing",
    "text": "It works.",
})
```

## Using templates

```python
emails = parcel_wing.emails.send(
    from_="Acme <hello@yourdomain.com>",
    to="person@example.com",
    template_alias="welcome_email",
    template_params={
        "first_name": "John",
    },
)
```

## Contacts

```python
contact = parcel_wing.contacts.create({
    "email": "person@example.com",
    "first_name": "John",
    "attributes": {
        "plan": "pro",
    },
})

page = parcel_wing.contacts.list(page=1, limit=20)

print(len(page["data"]), page.get("pagination", {}).get("total"))
```

Batch create contacts:

```python
result = parcel_wing.contacts.create([
    {"email": "one@example.com", "first_name": "One"},
    {"email": "two@example.com", "first_name": "Two"},
])

print(result["created"])
print(result["failed"])
```

## Segments

```python
segment = parcel_wing.segments.create({
    "name": "Pro plan users",
    "filter_criteria": {
        "version": 1,
        "match": "all",
        "conditions": [
            {
                "field": "attribute",
                "attribute_key": "plan",
                "operator": "equals",
                "value": "pro",
            },
        ],
    },
})
```

## Topics

```python
topic = parcel_wing.topics.create({
    "name": "Product Updates",
    "description": "Feature launches and release notes.",
    "default_subscription": "opt_in",
    "visibility": "public",
})
```

## Automation events

```python
parcel_wing.automations.track({
    "event_name": "user.completed_onboarding",
    "contact_id": "6d9dc8f7-c44e-4f2d-8a4e-d04f32f1744f",
    "payload": {
        "plan": "flight",
    },
})
```

## Error handling

```python
from parcelwing import ParcelWingError

try:
    parcel_wing.emails.send(
        from_="Acme <hello@yourdomain.com>",
        to="person@example.com",
        subject="Hello",
        text="Hi there",
    )
except ParcelWingError as error:
    print(error.status, error.type, error.code, error.request_id)
    print(error.details)
```

## Configuration

```python
parcel_wing = ParcelWing(
    api_key=os.environ["PARCEL_WING_API_KEY"],
    base_url="https://parcelwing.com",
    timeout=30.0,
)
```

Use the client as a context manager to close the underlying HTTP connection pool automatically:

```python
with ParcelWing(api_key=os.environ["PARCEL_WING_API_KEY"]) as parcel_wing:
    emails = parcel_wing.emails.send(
        from_="Acme <hello@yourdomain.com>",
        to="person@example.com",
        subject="Hello",
        text="It works.",
    )
```

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
mypy src/parcelwing
```

## Publishing

```bash
python -m pip install build twine
python -m build
twine upload dist/*
```
