import hashlib
import os
from contextlib import contextmanager
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from .models import (
    EvidenceCheckCreate,
    Execution,
    ExecutionApproval,
    MemoryEventCreate,
    Opportunity,
    OpportunityCreate,
)


class OpportunityNotFoundError(LookupError):
    """Raised when an operation targets an opportunity that does not exist."""


class ExecutionNotFoundError(LookupError):
    pass


class InvalidExecutionStateError(ValueError):
    pass


class Repository:
    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.environ["DATABASE_URL"]

    @contextmanager
    def connection(self):
        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            yield connection

    def health_status(self) -> dict[str, str | bool]:
        with self.connection() as connection:
            connection.execute("SELECT 1").fetchone()
        return {"status": "ok", "database": "connected", "demo": False}

    def create(self, payload: OpportunityCreate) -> Opportunity:
        opportunity_id = str(uuid4())
        event_id = str(uuid4())
        with self.connection() as connection, connection.transaction():
            row = connection.execute(
                """
                INSERT INTO opportunities
                    (id, name, reward_usd, deadline, confidence, status, next_action)
                VALUES (%s, %s, %s, %s, %s, 'candidate', %s)
                RETURNING *
                """,
                (
                    opportunity_id,
                    payload.name,
                    payload.reward_usd,
                    payload.deadline,
                    payload.confidence,
                    payload.next_action,
                ),
            ).fetchone()
            connection.execute(
                """INSERT INTO memory_events (id, opportunity_id, kind, detail)
                   VALUES (%s, %s, 'created', %s)""",
                (event_id, opportunity_id, f"Created opportunity: {payload.name}"),
            )
        return Opportunity.model_validate(row)

    def append_event(self, opportunity_id: str, payload: MemoryEventCreate):
        event_id = str(uuid4())
        with self.connection() as connection, connection.transaction():
            exists = connection.execute(
                "SELECT 1 FROM opportunities WHERE id = %s", (opportunity_id,)
            ).fetchone()
            if exists is None:
                raise OpportunityNotFoundError(opportunity_id)
            row = connection.execute(
                """INSERT INTO memory_events (id, opportunity_id, kind, detail)
                   VALUES (%s, %s, %s, %s) RETURNING *""",
                (event_id, opportunity_id, payload.kind, payload.detail),
            ).fetchone()
            if payload.status or payload.next_action:
                connection.execute(
                    """UPDATE opportunities SET
                       status = COALESCE(%s, status),
                       next_action = COALESCE(%s, next_action),
                       updated_at = now()
                       WHERE id = %s""",
                    (payload.status, payload.next_action, opportunity_id),
                )
        return row

    def memory(self, opportunity_id: str):
        with self.connection() as connection:
            exists = connection.execute(
                "SELECT 1 FROM opportunities WHERE id = %s", (opportunity_id,)
            ).fetchone()
            if exists is None:
                raise OpportunityNotFoundError(opportunity_id)
            return connection.execute(
                """SELECT * FROM memory_events WHERE opportunity_id = %s
                   ORDER BY created_at ASC""",
                (opportunity_id,),
            ).fetchall()

    def actionable(self):
        with self.connection() as connection:
            rows = connection.execute(
                """SELECT * FROM opportunities
                   WHERE status IN ('candidate', 'active', 'blocked')"""
            ).fetchall()
        return [Opportunity.model_validate(row) for row in rows]

    def plan_evidence_check(
        self, opportunity_id: str, payload: EvidenceCheckCreate
    ) -> Execution:
        execution_id = str(uuid4())
        actual_sha256 = hashlib.sha256(payload.evidence.encode("utf-8")).hexdigest()
        with self.connection() as connection, connection.transaction():
            if connection.execute(
                "SELECT 1 FROM opportunities WHERE id = %s", (opportunity_id,)
            ).fetchone() is None:
                raise OpportunityNotFoundError(opportunity_id)
            row = connection.execute(
                """INSERT INTO executions
                   (id, opportunity_id, action_kind, state, input)
                   VALUES (%s, %s, 'verify_evidence_sha256', 'planned', %s)
                   RETURNING *""",
                (
                    execution_id,
                    opportunity_id,
                    Jsonb(
                        {
                            "actual_sha256": actual_sha256,
                            "expected_sha256": payload.expected_sha256,
                            "evidence_bytes": len(payload.evidence.encode("utf-8")),
                        }
                    ),
                ),
            ).fetchone()
            connection.execute(
                """INSERT INTO memory_events (id, opportunity_id, kind, detail)
                   VALUES (%s, %s, 'progress', %s)""",
                (
                    str(uuid4()),
                    opportunity_id,
                    f"Planned evidence check {execution_id}; awaiting approval.",
                ),
            )
        return Execution.model_validate(row)

    def approve_execution(
        self, execution_id: str, payload: ExecutionApproval
    ) -> Execution:
        with self.connection() as connection, connection.transaction():
            row = connection.execute(
                "SELECT * FROM executions WHERE id = %s FOR UPDATE", (execution_id,)
            ).fetchone()
            if row is None:
                raise ExecutionNotFoundError(execution_id)
            if row["state"] != "planned":
                raise InvalidExecutionStateError("only planned executions can be approved")
            row = connection.execute(
                """UPDATE executions SET state = 'approved', approval_note = %s,
                   updated_at = now() WHERE id = %s RETURNING *""",
                (payload.note, execution_id),
            ).fetchone()
        return Execution.model_validate(row)

    def run_execution(self, execution_id: str) -> Execution:
        with self.connection() as connection, connection.transaction():
            row = connection.execute(
                "SELECT * FROM executions WHERE id = %s FOR UPDATE", (execution_id,)
            ).fetchone()
            if row is None:
                raise ExecutionNotFoundError(execution_id)
            if row["state"] != "approved":
                raise InvalidExecutionStateError("execution requires explicit approval")
            actual = row["input"]["actual_sha256"]
            matched = actual == row["input"]["expected_sha256"]
            state = "succeeded" if matched else "failed"
            result = {"matched": matched, "actual_sha256": actual}
            row = connection.execute(
                """UPDATE executions SET state = %s, result = %s,
                   updated_at = now() WHERE id = %s RETURNING *""",
                (state, Jsonb(result), execution_id),
            ).fetchone()
            connection.execute(
                """INSERT INTO memory_events (id, opportunity_id, kind, detail)
                   VALUES (%s, %s, %s, %s)""",
                (
                    str(uuid4()),
                    row["opportunity_id"],
                    "progress" if matched else "blocker",
                    f"Evidence check {execution_id} {state}; SHA-256 {actual}.",
                ),
            )
            connection.execute(
                """UPDATE opportunities SET status = %s, next_action = %s,
                   updated_at = now() WHERE id = %s""",
                (
                    "active" if matched else "blocked",
                    (
                        "Attach verified evidence to the submission"
                        if matched
                        else "Replace or regenerate mismatched evidence"
                    ),
                    row["opportunity_id"],
                ),
            )
        return Execution.model_validate(row)
