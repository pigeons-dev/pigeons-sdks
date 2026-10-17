from __future__ import annotations

from typing import Any, Generic, Literal, TypeVar
from typing_extensions import NotRequired, TypedDict

T = TypeVar("T")


# --- Pagination ---


class PaginatedResponse(TypedDict, Generic[T]):
    data: list[T]
    has_more: bool
    next_cursor: str | None


# --- Emails ---


class Email(TypedDict):
    id: str
    from_: NotRequired[str]
    to: list[str]
    cc: NotRequired[list[str]]
    bcc: NotRequired[list[str]]
    subject: str
    html: NotRequired[str]
    text: NotRequired[str]
    status: Literal["queued", "sending", "sent", "delivered", "bounced", "complained", "failed"]
    sesMessageId: NotRequired[str]
    tags: NotRequired[list[str]]
    headers: NotRequired[dict[str, str]]
    trackOpens: NotRequired[bool]
    openCount: NotRequired[int]
    firstOpenedAt: NotRequired[str]
    lastOpenedAt: NotRequired[str]
    scheduledAt: NotRequired[str]
    createdAt: str
    updatedAt: str


class SendEmailParams(TypedDict):
    to: str | list[str]
    from_: NotRequired[str]
    cc: NotRequired[list[str]]
    bcc: NotRequired[list[str]]
    subject: NotRequired[str]
    html: NotRequired[str]
    text: NotRequired[str]
    templateId: NotRequired[str]
    data: NotRequired[dict[str, Any]]
    tags: NotRequired[list[str]]
    headers: NotRequired[dict[str, str]]
    scheduledAt: NotRequired[str]
    trackOpens: NotRequired[bool]


class ListEmailsParams(TypedDict):
    cursor: NotRequired[str]
    limit: NotRequired[int]
    status: NotRequired[str]


# --- Domains ---


class DomainRecord(TypedDict):
    type: str
    name: str
    value: str
    ttl: int
    status: str
    purpose: str


class DomainCapabilities(TypedDict):
    sending: bool
    receiving: bool


class Domain(TypedDict):
    id: str
    domain: str
    verificationStatus: Literal["pending", "verified", "failed"]
    dkimTokens: NotRequired[list[str]]
    spfVerified: bool
    dmarcVerified: bool
    region: str
    capabilities: DomainCapabilities
    records: NotRequired[list[DomainRecord]]
    createdAt: str
    updatedAt: str


class AddDomainParams(TypedDict):
    domain: str
    capabilities: NotRequired[dict[str, bool]]


# --- API Keys ---


class ApiKey(TypedDict):
    id: str
    name: str
    prefix: str
    key: NotRequired[str]
    scopes: NotRequired[list[str]]
    expiresAt: NotRequired[str]
    lastUsedAt: NotRequired[str]
    createdAt: str


class CreateApiKeyParams(TypedDict):
    name: str
    scopes: NotRequired[list[str]]
    expiresAt: NotRequired[str]


# --- Templates ---


class Template(TypedDict):
    id: str
    slug: str
    name: str
    subject: str
    body: str
    sampleData: NotRequired[dict[str, Any]]
    version: int
    createdAt: str
    updatedAt: str


class CreateTemplateParams(TypedDict):
    slug: str
    name: str
    subject: str
    body: str
    sampleData: NotRequired[dict[str, Any]]


class UpdateTemplateParams(TypedDict):
    name: NotRequired[str]
    subject: NotRequired[str]
    body: NotRequired[str]
    sampleData: NotRequired[dict[str, Any]]


class TemplatePreview(TypedDict):
    subject: str
    html: str
    text: str


# --- Contacts ---


class Contact(TypedDict):
    id: str
    email: str
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    tags: NotRequired[list[str]]
    properties: NotRequired[dict[str, Any]]
    unsubscribed: bool
    unsubscribedAt: NotRequired[str]
    bounced: bool
    bouncedAt: NotRequired[str]
    complained: bool
    complainedAt: NotRequired[str]
    createdAt: str
    updatedAt: str


class CreateContactParams(TypedDict):
    email: str
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    tags: NotRequired[list[str]]
    properties: NotRequired[dict[str, Any]]


class UpdateContactParams(TypedDict):
    firstName: NotRequired[str]
    lastName: NotRequired[str]
    tags: NotRequired[list[str]]
    properties: NotRequired[dict[str, Any]]


class BatchCreateContactsResult(TypedDict):
    created: int
    skipped: int
    contacts: list[dict[str, str]]


class ListContactsParams(TypedDict):
    cursor: NotRequired[str]
    limit: NotRequired[int]
    tag: NotRequired[str]


# --- Inboxes ---


class Inbox(TypedDict):
    id: str
    name: str
    emailAddress: str
    description: NotRequired[str]
    webhookUrl: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]
    autoReplyEnabled: bool
    labels: NotRequired[list[str]]
    status: Literal["active", "paused", "archived"]
    catchAll: bool
    createdAt: str
    updatedAt: str


class CreateInboxParams(TypedDict):
    name: str
    emailAddress: NotRequired[str]
    description: NotRequired[str]
    webhookUrl: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]
    autoReplyEnabled: NotRequired[bool]
    labels: NotRequired[list[str]]


class UpdateInboxParams(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    webhookUrl: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]
    autoReplyEnabled: NotRequired[bool]
    labels: NotRequired[list[str]]


class ListInboxesParams(TypedDict):
    cursor: NotRequired[str]
    limit: NotRequired[int]
    status: NotRequired[str]
    labels: NotRequired[list[str]]


class InboxMessageAttachment(TypedDict):
    filename: str
    contentType: str
    size: int
    url: str


class InboxMessage(TypedDict):
    id: str
    inboxId: str
    direction: Literal["inbound", "outbound"]
    from_: NotRequired[str]
    to: list[str]
    subject: str
    html: NotRequired[str]
    text: NotRequired[str]
    extractedHtml: NotRequired[str]
    extractedText: NotRequired[str]
    threadId: str
    inReplyTo: NotRequired[str]
    labels: NotRequired[list[str]]
    attachments: NotRequired[list[InboxMessageAttachment]]
    sesMessageId: NotRequired[str]
    createdAt: str


class SendInboxMessageParams(TypedDict):
    to: str | list[str]
    subject: NotRequired[str]
    html: NotRequired[str]
    text: NotRequired[str]
    inReplyTo: NotRequired[str]
    labels: NotRequired[list[str]]


class ListInboxMessagesParams(TypedDict):
    cursor: NotRequired[str]
    limit: NotRequired[int]
    direction: NotRequired[str]
    threadId: NotRequired[str]
    labels: NotRequired[list[str]]


class Thread(TypedDict):
    id: str
    inboxId: str
    subject: str
    lastMessageAt: str
    messageCount: int
    participants: list[str]
    status: Literal["open", "closed", "snoozed"]
    metadata: NotRequired[dict[str, Any]]
    createdAt: str
    updatedAt: str


class UpdateThreadParams(TypedDict):
    status: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]


class ListThreadsParams(TypedDict):
    cursor: NotRequired[str]
    limit: NotRequired[int]
    status: NotRequired[str]


# --- Webhooks ---


class Webhook(TypedDict):
    id: str
    url: str
    events: list[str]
    secret: NotRequired[str]
    status: Literal["active", "disabled"]
    failureCount: int
    lastTriggeredAt: NotRequired[str]
    createdAt: str
    updatedAt: str


class CreateWebhookParams(TypedDict):
    url: str
    events: list[str]
    secret: NotRequired[str]


class UpdateWebhookParams(TypedDict):
    url: NotRequired[str]
    events: NotRequired[list[str]]
    secret: NotRequired[str]
    status: NotRequired[str]


class ListWebhooksParams(TypedDict):
    cursor: NotRequired[str]
    limit: NotRequired[int]


# --- Topics ---


class SubscriptionTopic(TypedDict):
    id: str
    name: str
    description: NotRequired[str]
    createdAt: str
    updatedAt: str


class CreateTopicParams(TypedDict):
    name: str
    description: NotRequired[str]


class UpdateTopicParams(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]


class ListTopicsParams(TypedDict):
    cursor: NotRequired[str]
    limit: NotRequired[int]


# --- Campaigns ---


class CampaignStats(TypedDict):
    total: int
    sent: int
    delivered: int
    opened: int
    bounced: int
    complained: int
    failed: int


class Campaign(TypedDict):
    id: str
    name: str
    subject: NotRequired[str]
    topicId: NotRequired[str]
    templateId: NotRequired[str]
    templateData: NotRequired[dict[str, Any]]
    fromName: NotRequired[str]
    fromEmail: NotRequired[str]
    audienceFilter: NotRequired[dict[str, Any]]
    status: Literal["draft", "scheduled", "sending", "paused", "sent", "cancelled"]
    scheduledAt: NotRequired[str]
    startedAt: NotRequired[str]
    completedAt: NotRequired[str]
    stats: CampaignStats
    createdAt: str
    updatedAt: str


class CreateCampaignParams(TypedDict):
    name: str
    subject: NotRequired[str]
    topicId: NotRequired[str]
    templateId: NotRequired[str]
    templateData: NotRequired[dict[str, Any]]
    fromName: NotRequired[str]
    fromEmail: NotRequired[str]
    audienceFilter: NotRequired[dict[str, Any]]
    scheduledAt: NotRequired[str]


class UpdateCampaignParams(TypedDict):
    name: NotRequired[str]
    subject: NotRequired[str]
    topicId: NotRequired[str]
    templateId: NotRequired[str]
    templateData: NotRequired[dict[str, Any]]
    fromName: NotRequired[str]
    fromEmail: NotRequired[str]
    audienceFilter: NotRequired[dict[str, Any]]
    scheduledAt: NotRequired[str]


class ListCampaignsParams(TypedDict):
    cursor: NotRequired[str]
    limit: NotRequired[int]
    status: NotRequired[str]


# --- Sequences ---


class SequenceStepStats(TypedDict):
    sent: int
    delivered: int
    opened: int
    bounced: int
    complained: int


class SequenceStep(TypedDict):
    id: str
    sequenceId: str
    position: int
    type: Literal["email", "delay", "condition"]
    topicId: NotRequired[str]
    templateId: NotRequired[str]
    templateData: NotRequired[dict[str, Any]]
    subject: NotRequired[str]
    delayDuration: NotRequired[str]
    condition: NotRequired[dict[str, Any]]
    stats: SequenceStepStats
    createdAt: str
    updatedAt: str


class SequenceStats(TypedDict):
    enrolled: int
    completed: int
    exited: int
    active: int


class SequenceTrigger(TypedDict):
    event: str
    filter: NotRequired[dict[str, Any]]


class Sequence(TypedDict):
    id: str
    name: str
    trigger: NotRequired[SequenceTrigger]
    status: Literal["draft", "active", "paused", "archived"]
    stats: SequenceStats
    steps: NotRequired[list[SequenceStep]]
    createdAt: str
    updatedAt: str


class CreateSequenceStepParams(TypedDict):
    type: Literal["email", "delay", "condition"]
    topicId: NotRequired[str]
    templateId: NotRequired[str]
    templateData: NotRequired[dict[str, Any]]
    subject: NotRequired[str]
    delayDuration: NotRequired[str]
    condition: NotRequired[dict[str, Any]]


class CreateSequenceParams(TypedDict):
    name: str
    trigger: NotRequired[SequenceTrigger]
    steps: NotRequired[list[CreateSequenceStepParams]]


class UpdateSequenceParams(TypedDict):
    name: NotRequired[str]
    trigger: NotRequired[SequenceTrigger]
    steps: NotRequired[list[CreateSequenceStepParams]]


class ListSequencesParams(TypedDict):
    cursor: NotRequired[str]
    limit: NotRequired[int]
    status: NotRequired[str]


class SequenceEnrollment(TypedDict):
    id: str
    sequenceId: str
    contactId: str
    currentStepId: NotRequired[str]
    status: Literal["active", "completed", "exited", "failed"]
    enrolledAt: str
    completedAt: NotRequired[str]
    createdAt: str
    updatedAt: str


# --- Stats ---


class PeriodStats(TypedDict):
    sent: int
    delivered: int
    opened: int
    bounced: int
    complained: int
    failed: int
    deliveryRate: float
    bounceRate: float
    complaintRate: float
    openRate: float


class WarmupGuidance(TypedDict):
    phase: Literal["new", "warming", "established"]
    dailyLimit: int
    recommendation: str


class DomainStats(TypedDict):
    domainId: str
    domain: str
    last24h: PeriodStats
    last7d: PeriodStats
    last30d: PeriodStats
    warmup: WarmupGuidance


class TopDomain(TypedDict):
    domain: str
    sent: int
    deliveryRate: float


class GlobalStats(TypedDict):
    last24h: PeriodStats
    last7d: PeriodStats
    last30d: PeriodStats
    topDomains: list[TopDomain]
