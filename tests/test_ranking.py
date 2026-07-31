from datetime import datetime, timedelta, timezone

from app.models import Opportunity
from app.ranking import rank_action


def opportunity(**overrides):
    now = datetime.now(timezone.utc)
    values = {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "Example",
        "reward_usd": 1000,
        "deadline": now + timedelta(hours=24),
        "confidence": 0.5,
        "status": "active",
        "next_action": "Build baseline",
        "created_at": now,
        "updated_at": now,
    }
    values.update(overrides)
    return Opportunity(**values)


def test_nearer_deadline_scores_higher():
    now = datetime.now(timezone.utc)
    near = rank_action(opportunity(deadline=now + timedelta(hours=12)), now)
    far = rank_action(opportunity(deadline=now + timedelta(days=30)), now)
    assert near.urgency_score > far.urgency_score


def test_blocker_reduces_priority():
    now = datetime.now(timezone.utc)
    active = rank_action(opportunity(status="active"), now)
    blocked = rank_action(opportunity(status="blocked"), now)
    assert active.urgency_score > blocked.urgency_score
