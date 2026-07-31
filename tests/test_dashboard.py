from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_exposes_demo_workflow() -> None:
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert "Opportunity Memory Agent" in response.text
    assert "Add opportunity" in response.text
    assert "Ranked action queue" in response.text
    assert "Append immutable event" in response.text
    assert "Grounded Gemini brief" in response.text
