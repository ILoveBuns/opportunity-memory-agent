from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.demo_repository import DemoRepository
from app.main import app, get_repository
from app.models import MemoryEventCreate, OpportunityCreate


def payload(name: str = "Demo opportunity") -> OpportunityCreate:
    return OpportunityCreate(
        name=name,
        reward_usd=250,
        deadline=datetime.now(timezone.utc) + timedelta(days=1),
        confidence=0.9,
        next_action="Verify evidence",
    )


def test_demo_repository_preserves_timeline_and_updates_state() -> None:
    repository = DemoRepository()
    opportunity = repository.create(payload())

    event = repository.append_event(
        opportunity.id,
        MemoryEventCreate(
            kind="progress",
            detail="Tests passed",
            status="active",
            next_action="Publish evidence",
        ),
    )

    assert [item.kind for item in repository.memory(opportunity.id)] == [
        "created",
        "progress",
    ]
    assert event.detail == "Tests passed"
    current = repository.actionable()[0]
    assert current.status == "active"
    assert current.next_action == "Publish evidence"


def test_demo_repository_drives_real_health_and_actions_endpoints() -> None:
    repository = DemoRepository()
    repository.create(payload("Runnable product demo"))
    app.dependency_overrides[get_repository] = lambda: repository
    try:
        client = TestClient(app)
        assert client.get("/health").json() == {
            "status": "ok",
            "database": "in-memory demo",
            "demo": True,
        }
        actions = client.get("/actions").json()
    finally:
        app.dependency_overrides.clear()

    assert len(actions) == 1
    assert actions[0]["opportunity"]["name"] == "Runnable product demo"
