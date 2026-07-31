# Opportunity Memory Agent

An agentic opportunity tracker that remembers every review, blocker, deadline, and
next action in CockroachDB. It is designed for the CockroachDB × AWS Agentic
Memory hackathon.

## Why persistent memory matters

Opportunity workflows span weeks: organizers reply, deadlines move, credentials
expire, and a previously blocked task may become actionable. A stateless chatbot
repeats work or misses deadlines. This service stores an append-only event history
and derives a prioritized action queue from that history.

## Local run

1. Start a CockroachDB instance and create a database.
2. Copy `.env.example` to `.env` and set `DATABASE_URL`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Initialize the schema: `python -m app.init_db`.
5. Run: `uvicorn app.main:app --reload`.

Open `http://localhost:8000/` for the responsive demo dashboard. The interactive
page creates opportunities, displays the ranked queue, appends memory events,
shows the durable timeline, and requests a grounded Gemini brief without adding
a frontend framework or build step.

For a reproducible container demo, set `GEMINI_API_KEY` and run
`docker compose up --build`. After the services are healthy, run
`docker compose exec api python scripts/seed_demo.py` (the script is included in
the repository and may also be run directly against any configured database).

The production target is AWS App Runner or ECS backed by CockroachDB Cloud. No
cloud resources are created by this repository.

## API

- `POST /opportunities` creates an opportunity and its first memory event.
- `POST /opportunities/{id}/events` appends a review, progress, or blocker event.
- `GET /opportunities/{id}/memory` returns the complete durable timeline.
- `GET /actions` ranks the next actions using deadline, status, and confidence.
- `GET /actions/brief` asks Gemini for an evidence-grounded Markdown action brief.
- `GET /health` reports service and database health.

The Gemini integration receives only the ten highest-ranked opportunity records
and is instructed not to invent eligibility, progress, or rewards. Set
`GEMINI_API_KEY`; `GEMINI_MODEL` defaults to `gemini-2.5-flash`.

## Tests

Run `pytest`.

See `SUBMISSION_DRAFT.md` for the sponsor mapping, evidence checklist, and the
under-three-minute demo sequence. The draft deliberately leaves cloud and
customer-validation claims unfilled until they can be demonstrated.

## License

MIT
