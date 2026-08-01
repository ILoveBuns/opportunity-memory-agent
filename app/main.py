from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .dashboard import DASHBOARD_HTML
from .gemini import generate_action_brief
from .models import MemoryEvent, MemoryEventCreate, Opportunity, OpportunityCreate, RankedAction
from .ranking import rank_action
from .repository import OpportunityNotFoundError, Repository

app = FastAPI(title="Opportunity Memory Agent", version="0.1.0")


def get_repository() -> Repository:
    return Repository()


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard():
    return DASHBOARD_HTML


@app.get("/health")
def health(repository: Repository = Depends(get_repository)):
    try:
        with repository.connection() as connection:
            connection.execute("SELECT 1").fetchone()
        return {"status": "ok", "database": "connected"}
    except Exception as error:
        raise HTTPException(status_code=503, detail="database unavailable") from error


@app.post("/opportunities", response_model=Opportunity, status_code=201)
def create_opportunity(
    payload: OpportunityCreate, repository: Repository = Depends(get_repository)
):
    return repository.create(payload)


@app.post("/opportunities/{opportunity_id}/events", response_model=MemoryEvent)
def append_event(
    opportunity_id: str,
    payload: MemoryEventCreate,
    repository: Repository = Depends(get_repository),
):
    try:
        return repository.append_event(opportunity_id, payload)
    except OpportunityNotFoundError as error:
        raise HTTPException(status_code=404, detail="opportunity not found") from error


@app.get("/opportunities/{opportunity_id}/memory", response_model=list[MemoryEvent])
def get_memory(opportunity_id: str, repository: Repository = Depends(get_repository)):
    try:
        return repository.memory(opportunity_id)
    except OpportunityNotFoundError as error:
        raise HTTPException(status_code=404, detail="opportunity not found") from error


@app.get("/actions", response_model=list[RankedAction])
def get_actions(repository: Repository = Depends(get_repository)):
    return sorted(
        (rank_action(item) for item in repository.actionable()),
        key=lambda action: action.urgency_score,
        reverse=True,
    )


@app.get("/actions/brief")
def get_action_brief(repository: Repository = Depends(get_repository)):
    actions = sorted(
        (rank_action(item) for item in repository.actionable()),
        key=lambda action: action.urgency_score,
        reverse=True,
    )
    try:
        return {"brief": generate_action_brief(actions), "action_count": len(actions)}
    except ValueError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
