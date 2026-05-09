"""Type definitions for the Parcel Wing API."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

NullablePrimitive = Union[str, int, float, bool, None]
JsonObject = Dict[str, Any]


class Pagination(TypedDict):
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


class ListResponse(TypedDict, total=False):
    object: Literal["list"]
    data: List[Any]
    pagination: Pagination


class DeletionResponse(TypedDict):
    object: str
    id: str
    deleted: Literal[True]


class ApiErrorPayload(TypedDict, total=False):
    type: str
    code: str
    message: str
    details: Any
    request_id: str


ContactStatus = Literal[
    "active", "unsubscribed", "bounced", "spam_complaint", "inactive"
]


class Contact(TypedDict, total=False):
    object: Literal["contact"]
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    attributes: Dict[str, NullablePrimitive]
    status: ContactStatus
    source: Optional[str]
    external_id: Optional[str]
    metadata: JsonObject
    created_at: str
    updated_at: str
    subscribed_at: Optional[str]
    unsubscribed_at: Optional[str]


class ContactCreateRequest(TypedDict, total=False):
    email: str
    first_name: str
    last_name: str
    attributes: Dict[str, NullablePrimitive]
    status: ContactStatus
    external_id: str
    metadata: JsonObject


ContactUpdateRequest = ContactCreateRequest


class ContactListParams(TypedDict, total=False):
    page: int
    limit: int
    status: ContactStatus
    search: str
    external_id: str
    sort_by: Literal["created_at", "updated_at", "email", "first_name", "last_name"]
    sort_order: Literal["asc", "desc"]


class BatchCreateContactsResult(TypedDict):
    created: List[Contact]
    failed: List[Dict[str, str]]


SegmentFilterField = Literal[
    "email",
    "first_name",
    "last_name",
    "full_name",
    "status",
    "source",
    "external_id",
    "created_at",
    "updated_at",
    "subscribed_at",
    "unsubscribed_at",
    "attribute",
]
SegmentFilterOperator = Literal[
    "equals",
    "not_equals",
    "contains",
    "not_contains",
    "starts_with",
    "ends_with",
    "is_empty",
    "is_not_empty",
    "before",
    "after",
    "on_or_before",
    "on_or_after",
]


class SegmentFilterCondition(TypedDict, total=False):
    id: str
    field: SegmentFilterField
    operator: SegmentFilterOperator
    value: Union[str, int, float, bool]
    attribute_key: str


class SegmentFilterCriteria(TypedDict):
    version: Literal[1]
    match: Literal["all", "any"]
    conditions: List[SegmentFilterCondition]


class Segment(TypedDict, total=False):
    object: Literal["segment"]
    id: str
    name: str
    description: Optional[str]
    filter_criteria: SegmentFilterCriteria
    type: Optional[str]
    contact_count: int
    is_active: bool
    metadata: Optional[JsonObject]
    created_at: str
    updated_at: str


class SegmentCreateRequest(TypedDict, total=False):
    name: str
    description: str
    filter_criteria: SegmentFilterCriteria
    is_active: bool


SegmentUpdateRequest = SegmentCreateRequest


class SegmentListParams(TypedDict, total=False):
    page: int
    limit: int
    search: str
    active: bool
    include_counts: bool
    sort_by: Literal["created_at", "updated_at", "name"]
    sort_order: Literal["asc", "desc"]


TopicDefaultSubscription = Literal["opt_in", "opt_out"]
TopicVisibility = Literal["public", "private"]


class Topic(TypedDict, total=False):
    object: Literal["topic"]
    id: str
    name: str
    description: Optional[str]
    default_subscription: TopicDefaultSubscription
    visibility: TopicVisibility
    is_active: bool
    subscriber_count: int
    explicit_subscriber_count: int
    explicit_unsubscriber_count: int
    created_at: str
    updated_at: str


class TopicCreateRequest(TypedDict, total=False):
    name: str
    description: str
    default_subscription: TopicDefaultSubscription
    visibility: TopicVisibility
    is_active: bool


class TopicUpdateRequest(TypedDict, total=False):
    name: str
    description: str
    visibility: TopicVisibility
    is_active: bool


class TopicListParams(TypedDict, total=False):
    page: int
    limit: int
    search: str
    active: bool
    visibility: TopicVisibility
    sort_by: Literal["created_at", "updated_at", "name"]
    sort_order: Literal["asc", "desc"]


class EmailSendRequest(TypedDict, total=False):
    from_: str
    to: Union[str, List[str]]
    subject: str
    text: str
    html: str
    reply_to: str
    tags: Dict[str, str]
    template_id: str
    template_alias: str
    template_params: Dict[str, NullablePrimitive]


class QueuedEmail(TypedDict):
    object: Literal["email"]
    id: str
    to: str
    status: Literal["queued"]


class AutomationTrackRequest(TypedDict, total=False):
    event_name: str
    contact_id: Optional[str]
    payload: Dict[str, Any]
    event_id: str


class AutomationEvent(TypedDict, total=False):
    object: Literal["automation_event"]
    event_id: str
    event_name: str
    contact_id: Optional[str]
    queued_runs: int
