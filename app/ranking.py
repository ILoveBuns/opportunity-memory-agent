from datetime import datetime, timezone

from .models import Opportunity, RankedAction


def rank_action(item: Opportunity, now: datetime | None = None) -> RankedAction:
    now = now or datetime.now(timezone.utc)
    deadline_score = 0.0
    reason = "No deadline; ranked by reward and confidence."
    if item.deadline:
        deadline = item.deadline
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        hours = max((deadline - now).total_seconds() / 3600, 1)
        deadline_score = min(100, 2400 / hours)
        reason = f"Deadline is in {hours:.1f} hours."

    reward_score = min(item.reward_usd / 1000, 50)
    status_adjustment = {"active": 15, "candidate": 5, "blocked": -20}.get(
        item.status, -50
    )
    score = deadline_score + reward_score * item.confidence + status_adjustment
    return RankedAction(opportunity=item, urgency_score=round(score, 2), reason=reason)
