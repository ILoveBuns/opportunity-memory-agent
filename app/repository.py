import os
from contextlib import contextmanager
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row

from .models import MemoryEventCreate, Opportunity, OpportunityCreate


class Repository:
    def __init__(self, database_url: str | None = None):
        self.database_url = database_url or os.environ["DATABASE_URL"]

    @contextmanager
    def connection(self):
        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            yield connection

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
