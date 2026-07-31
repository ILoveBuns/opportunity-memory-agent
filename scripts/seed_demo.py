"""Seed a small, truthful opportunity timeline for a local demonstration."""

from datetime import datetime, timedelta, timezone

from app.models import MemoryEventCreate, OpportunityCreate
from app.repository import Repository


def main() -> None:
    repository = Repository()
    deadline = datetime.now(timezone.utc) + timedelta(days=3)
    opportunity = repository.create(
        OpportunityCreate(
            name="Agentic Memory demo submission",
            reward_usd=8750,
            deadline=deadline,
            confidence=0.55,
            next_action="Deploy the tested service to AWS",
        )
    )
    repository.append_event(
        opportunity.id,
        MemoryEventCreate(
            kind="progress",
            detail="Implemented durable CockroachDB event memory and deterministic ranking.",
            status="active",
            next_action="Record the deployed end-to-end demo",
        ),
    )
    repository.append_event(
        opportunity.id,
        MemoryEventCreate(
            kind="blocker",
            detail="Cloud deployment credentials are not configured in this environment.",
            status="blocked",
            next_action="Configure AWS and CockroachDB Cloud credentials",
        ),
    )
    print(opportunity.id)


if __name__ == "__main__":
    main()
