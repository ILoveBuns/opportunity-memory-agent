import json
from datetime import datetime, timezone

import pytest

from app.gemini import build_action_prompt, generate_action_brief
from app.models import Opportunity, RankedAction


def action() -> RankedAction:
    now = datetime.now(timezone.utc)
    opportunity = Opportunity(
        id="00000000-0000-0000-0000-000000000001",
        name="Small contest",
        reward_usd=500,
        deadline=now,
        confidence=0.8,
        status="active",
        next_action="Run the baseline",
        created_at=now,
        updated_at=now,
    )
    return RankedAction(opportunity=opportunity, urgency_score=42, reason="Soon")


def test_prompt_contains_grounded_action_fields():
    prompt = build_action_prompt([action()])
    assert "Small contest" in prompt
    assert "Run the baseline" in prompt
    assert "Never invent" in prompt


def test_generate_action_brief_parses_gemini_response():
    def transport(request, timeout):
        assert "gemini-test:generateContent" in request.full_url
        assert timeout == 30
        request_payload = json.loads(request.data)
        assert "Small contest" in request_payload["contents"][0]["parts"][0]["text"]
        return json.dumps(
            {"candidates": [{"content": {"parts": [{"text": "Do the baseline."}]}}]}
        ).encode()

    assert (
        generate_action_brief(
            [action()], api_key="test-key", model="gemini-test", transport=transport
        )
        == "Do the baseline."
    )


def test_generate_action_brief_requires_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        generate_action_brief([action()])
