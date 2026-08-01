from fastapi.testclient import TestClient

from app.main import app, get_repository
from app.repository import OpportunityNotFoundError


def test_dashboard_exposes_demo_workflow() -> None:
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert "Opportunity Memory Agent" in response.text
    assert "Add opportunity" in response.text
    assert "Ranked action queue" in response.text
    assert "Append immutable event" in response.text
    assert "Grounded Gemini brief" in response.text


class MissingOpportunityRepository:
    def append_event(self, opportunity_id, payload):
        raise OpportunityNotFoundError(opportunity_id)

    def memory(self, opportunity_id):
        raise OpportunityNotFoundError(opportunity_id)


def test_append_event_for_missing_opportunity_returns_404() -> None:
    app.dependency_overrides[get_repository] = lambda: MissingOpportunityRepository()
    try:
        response = TestClient(app).post(
            "/opportunities/00000000-0000-0000-0000-000000000099/events",
            json={"kind": "progress", "detail": "Prepared evidence"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {"detail": "opportunity not found"}


def test_memory_for_missing_opportunity_returns_404() -> None:
    app.dependency_overrides[get_repository] = lambda: MissingOpportunityRepository()
    try:
        response = TestClient(app).get(
            "/opportunities/00000000-0000-0000-0000-000000000099/memory"
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {"detail": "opportunity not found"}
