import json
import os
from collections.abc import Callable
from urllib.request import Request, urlopen

from .models import RankedAction


Transport = Callable[[Request, float], bytes]


def _default_transport(request: Request, timeout: float) -> bytes:
    with urlopen(request, timeout=timeout) as response:  # noqa: S310
        return response.read()


def build_action_prompt(actions: list[RankedAction]) -> str:
    """Create a bounded prompt from ranked, database-backed opportunity memory."""
    facts = [
        {
            "name": action.opportunity.name,
            "status": action.opportunity.status,
            "reward_usd": action.opportunity.reward_usd,
            "deadline": action.opportunity.deadline.isoformat()
            if action.opportunity.deadline
            else None,
            "next_action": action.opportunity.next_action,
            "urgency_score": action.urgency_score,
            "ranking_reason": action.reason,
        }
        for action in actions[:10]
    ]
    return (
        "You are an opportunity operations agent. Use only the supplied JSON facts. "
        "Return a concise Markdown brief with: top 3 actions, blockers, and deadlines. "
        "Never invent eligibility, progress, or rewards.\n\n"
        + json.dumps(facts, ensure_ascii=False)
    )


def generate_action_brief(
    actions: list[RankedAction],
    *,
    api_key: str | None = None,
    model: str | None = None,
    transport: Transport = _default_transport,
) -> str:
    """Generate an evidence-grounded action brief with the Gemini API."""
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY is required")

    selected_model = model or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{selected_model}:generateContent?key={key}"
    )
    body = json.dumps(
        {"contents": [{"parts": [{"text": build_action_prompt(actions)}]}]}
    ).encode("utf-8")
    request = Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    payload = json.loads(transport(request, 30).decode("utf-8"))
    try:
        return payload["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Gemini returned no text candidate") from error
