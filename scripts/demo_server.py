"""Run the real dashboard and API with clearly labelled synthetic demo data."""

from datetime import datetime, timedelta, timezone

from app.demo_repository import DemoRepository
from app.main import app, get_repository
from app.models import MemoryEventCreate, OpportunityCreate


repository = DemoRepository()
now = datetime.now(timezone.utc)

review = repository.create(
    OpportunityCreate(
        name="GOAI submission review",
        reward_usd=5000,
        deadline=now + timedelta(days=6),
        confidence=0.75,
        next_action="Wait for organizer review",
    )
)
repository.append_event(
    review.id,
    MemoryEventCreate(
        kind="submission",
        detail="Synthetic demo: submission package recorded for organizer review.",
        status="blocked",
        next_action="Resume only when organizer evidence arrives",
    ),
)

urgent = repository.create(
    OpportunityCreate(
        name="Reproducibility evidence",
        reward_usd=250,
        deadline=now + timedelta(hours=18),
        confidence=0.95,
        next_action="Run tests and attach the evidence manifest",
    )
)
repository.append_event(
    urgent.id,
    MemoryEventCreate(
        kind="progress",
        detail="Synthetic demo: source, tests, and artifact hashes are ready.",
        status="active",
    ),
)

app.dependency_overrides[get_repository] = lambda: repository
