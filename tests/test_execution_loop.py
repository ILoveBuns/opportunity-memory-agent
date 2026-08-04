import hashlib
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.demo_repository import DemoRepository
from app.main import app, get_repository
from app.models import OpportunityCreate


def make_opportunity(repository: DemoRepository):
    return repository.create(
        OpportunityCreate(
            name="Evidence delivery",
            reward_usd=500,
            deadline=datetime.now(timezone.utc) + timedelta(days=1),
            confidence=0.8,
            next_action="Verify artifact",
        )
    )


def test_execution_requires_approval_and_writes_verified_result_to_memory() -> None:
    repository = DemoRepository()
    opportunity = make_opportunity(repository)
    evidence = "reproducible artifact"
    expected = hashlib.sha256(evidence.encode()).hexdigest()
    app.dependency_overrides[get_repository] = lambda: repository
    try:
        client = TestClient(app)
        planned = client.post(
            f"/opportunities/{opportunity.id}/executions/evidence-check",
            json={"evidence": evidence, "expected_sha256": expected},
        ).json()
        assert "evidence" not in planned["input"]
        assert planned["input"]["evidence_bytes"] == len(evidence.encode())
        blocked = client.post(f"/executions/{planned['id']}/run")
        approved = client.post(
            f"/executions/{planned['id']}/approve",
            json={"note": "Human reviewed the bounded checksum action"},
        )
        completed = client.post(f"/executions/{planned['id']}/run")
        memory = client.get(f"/opportunities/{opportunity.id}/memory").json()
    finally:
        app.dependency_overrides.clear()

    assert blocked.status_code == 409
    assert approved.json()["state"] == "approved"
    assert completed.status_code == 200
    assert completed.json()["state"] == "succeeded"
    assert completed.json()["result"] == {
        "matched": True,
        "actual_sha256": expected,
    }
    assert any("succeeded" in event["detail"] for event in memory)


def test_mismatch_fails_closed_and_blocks_opportunity() -> None:
    repository = DemoRepository()
    opportunity = make_opportunity(repository)
    app.dependency_overrides[get_repository] = lambda: repository
    try:
        client = TestClient(app)
        planned = client.post(
            f"/opportunities/{opportunity.id}/executions/evidence-check",
            json={"evidence": "changed", "expected_sha256": "0" * 64},
        ).json()
        client.post(
            f"/executions/{planned['id']}/approve",
            json={"note": "Approved deterministic verification"},
        )
        result = client.post(f"/executions/{planned['id']}/run").json()
        action = client.get("/actions").json()[0]["opportunity"]
    finally:
        app.dependency_overrides.clear()

    assert result["state"] == "failed"
    assert result["result"]["matched"] is False
    assert action["status"] == "blocked"
    assert action["next_action"] == "Replace or regenerate mismatched evidence"
