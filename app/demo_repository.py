"""In-memory repository used only for the reproducible product demo."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
from threading import RLock
from uuid import uuid4

from .models import (
    EvidenceCheckCreate,
    Execution,
    ExecutionApproval,
    MemoryEvent,
    MemoryEventCreate,
    Opportunity,
    OpportunityCreate,
)
from .repository import (
    ExecutionNotFoundError,
    InvalidExecutionStateError,
    OpportunityNotFoundError,
)


class _HealthyCursor:
    def fetchone(self) -> tuple[int]:
        return (1,)


class _HealthyConnection:
    def execute(self, _query: str) -> _HealthyCursor:
        return _HealthyCursor()


class DemoRepository:
    """Process-local store that exercises the real API and dashboard.

    This deliberately does not pretend to demonstrate persistence. Production
    and container runs continue to use CockroachDB through ``Repository``.
    """

    def __init__(self) -> None:
        self._opportunities: dict[str, Opportunity] = {}
        self._events: dict[str, list[MemoryEvent]] = {}
        self._executions: dict[str, Execution] = {}
        self._lock = RLock()

    @contextmanager
    def connection(self):
        yield _HealthyConnection()

    def health_status(self) -> dict[str, str | bool]:
        return {"status": "ok", "database": "in-memory demo", "demo": True}

    def create(self, payload: OpportunityCreate) -> Opportunity:
        with self._lock:
            now = datetime.now(timezone.utc)
            opportunity = Opportunity(
                id=str(uuid4()),
                name=payload.name,
                reward_usd=payload.reward_usd,
                deadline=payload.deadline,
                confidence=payload.confidence,
                status="candidate",
                next_action=payload.next_action,
                created_at=now,
                updated_at=now,
            )
            event = MemoryEvent(
                id=str(uuid4()),
                opportunity_id=opportunity.id,
                kind="created",
                detail=f"Created opportunity: {payload.name}",
                created_at=now,
            )
            self._opportunities[opportunity.id] = opportunity
            self._events[opportunity.id] = [event]
            return opportunity

    def append_event(
        self, opportunity_id: str, payload: MemoryEventCreate
    ) -> MemoryEvent:
        with self._lock:
            opportunity = self._opportunities.get(opportunity_id)
            if opportunity is None:
                raise OpportunityNotFoundError(opportunity_id)
            now = datetime.now(timezone.utc)
            event = MemoryEvent(
                id=str(uuid4()),
                opportunity_id=opportunity_id,
                kind=payload.kind,
                detail=payload.detail,
                created_at=now,
            )
            self._events[opportunity_id].append(event)
            updates = {"updated_at": now}
            if payload.status is not None:
                updates["status"] = payload.status
            if payload.next_action is not None:
                updates["next_action"] = payload.next_action
            self._opportunities[opportunity_id] = opportunity.model_copy(update=updates)
            return event

    def memory(self, opportunity_id: str) -> list[MemoryEvent]:
        with self._lock:
            if opportunity_id not in self._opportunities:
                raise OpportunityNotFoundError(opportunity_id)
            return list(self._events[opportunity_id])

    def actionable(self) -> list[Opportunity]:
        with self._lock:
            return [
                item
                for item in self._opportunities.values()
                if item.status in {"candidate", "active", "blocked"}
            ]

    def plan_evidence_check(
        self, opportunity_id: str, payload: EvidenceCheckCreate
    ) -> Execution:
        with self._lock:
            if opportunity_id not in self._opportunities:
                raise OpportunityNotFoundError(opportunity_id)
            now = datetime.now(timezone.utc)
            actual_sha256 = hashlib.sha256(payload.evidence.encode("utf-8")).hexdigest()
            execution = Execution(
                id=str(uuid4()),
                opportunity_id=opportunity_id,
                action_kind="verify_evidence_sha256",
                state="planned",
                input={
                    "actual_sha256": actual_sha256,
                    "expected_sha256": payload.expected_sha256,
                    "evidence_bytes": len(payload.evidence.encode("utf-8")),
                },
                created_at=now,
                updated_at=now,
            )
            self._executions[execution.id] = execution
            self.append_event(
                opportunity_id,
                MemoryEventCreate(
                    kind="progress",
                    detail=f"Planned evidence check {execution.id}; awaiting approval.",
                ),
            )
            return execution

    def approve_execution(
        self, execution_id: str, payload: ExecutionApproval
    ) -> Execution:
        with self._lock:
            execution = self._executions.get(execution_id)
            if execution is None:
                raise ExecutionNotFoundError(execution_id)
            if execution.state != "planned":
                raise InvalidExecutionStateError("only planned executions can be approved")
            execution = execution.model_copy(
                update={
                    "state": "approved",
                    "approval_note": payload.note,
                    "updated_at": datetime.now(timezone.utc),
                }
            )
            self._executions[execution_id] = execution
            return execution

    def run_execution(self, execution_id: str) -> Execution:
        with self._lock:
            execution = self._executions.get(execution_id)
            if execution is None:
                raise ExecutionNotFoundError(execution_id)
            if execution.state != "approved":
                raise InvalidExecutionStateError("execution requires explicit approval")
            actual = execution.input["actual_sha256"]
            matched = actual == execution.input["expected_sha256"]
            state = "succeeded" if matched else "failed"
            execution = execution.model_copy(
                update={
                    "state": state,
                    "result": {"matched": matched, "actual_sha256": actual},
                    "updated_at": datetime.now(timezone.utc),
                }
            )
            self._executions[execution_id] = execution
            self.append_event(
                execution.opportunity_id,
                MemoryEventCreate(
                    kind="progress" if matched else "blocker",
                    detail=f"Evidence check {execution.id} {state}; SHA-256 {actual}.",
                    status="active" if matched else "blocked",
                    next_action=(
                        "Attach verified evidence to the submission"
                        if matched
                        else "Replace or regenerate mismatched evidence"
                    ),
                ),
            )
            return execution
