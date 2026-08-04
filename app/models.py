from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


Status = Literal["candidate", "active", "blocked", "submitted", "closed"]
EventKind = Literal["created", "review", "progress", "blocker", "submission"]
ExecutionState = Literal["planned", "approved", "succeeded", "failed"]


class OpportunityCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    reward_usd: int = Field(ge=0)
    deadline: datetime | None = None
    confidence: float = Field(default=0.5, ge=0, le=1)
    next_action: str = Field(min_length=2, max_length=500)


class MemoryEventCreate(BaseModel):
    kind: EventKind
    detail: str = Field(min_length=2, max_length=2000)
    status: Status | None = None
    next_action: str | None = Field(default=None, max_length=500)


class Opportunity(BaseModel):
    id: str
    name: str
    reward_usd: int
    deadline: datetime | None
    confidence: float
    status: Status
    next_action: str
    created_at: datetime
    updated_at: datetime


class MemoryEvent(BaseModel):
    id: str
    opportunity_id: str
    kind: EventKind
    detail: str
    created_at: datetime


class RankedAction(BaseModel):
    opportunity: Opportunity
    urgency_score: float
    reason: str


class EvidenceCheckCreate(BaseModel):
    """A deliberately bounded, deterministic closed-loop action."""

    evidence: str = Field(min_length=1, max_length=100_000)
    expected_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class ExecutionApproval(BaseModel):
    note: str = Field(min_length=2, max_length=500)


class Execution(BaseModel):
    id: str
    opportunity_id: str
    action_kind: Literal["verify_evidence_sha256"]
    state: ExecutionState
    input: dict[str, Any]
    result: dict[str, Any] | None = None
    approval_note: str | None = None
    created_at: datetime
    updated_at: datetime
