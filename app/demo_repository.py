"""In-memory repository used only for the reproducible product demo."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4

from .models import MemoryEvent, MemoryEventCreate, Opportunity, OpportunityCreate
from .repository import OpportunityNotFoundError


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
