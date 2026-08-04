# Opportunity Memory Agent

An agentic opportunity tracker that remembers every review, blocker, deadline, and
next action in CockroachDB. The reusable open-source core targets long-running,
real-world agent workflows; it is also packaged for the CockroachDB × AWS Agentic
Memory hackathon and GOAI 2026 Boundless Agents track.

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

For a zero-credential product walkthrough, run:

```bash
uvicorn scripts.demo_server:app --reload
```

This serves the real dashboard and API with explicitly labelled synthetic,
process-local data. It demonstrates creation, immutable event append, timeline
inspection, and ranked actions without claiming CockroachDB persistence. Use the
Docker Compose workflow above when demonstrating durable storage.

For a reproducible container demo, set `GEMINI_API_KEY` and run
`docker compose up --build`. After the services are healthy, run
`docker compose exec api python scripts/seed_demo.py` (the script is included in
the repository and may also be run directly against any configured database).

The production target is AWS App Runner backed by CockroachDB Cloud. The
checked-in `apprunner.yaml` contains no credentials; the deployment guide maps
account-specific Secrets Manager ARNs in the service configuration. See
`DEPLOYMENT.md` for the deployment and evidence checklist. No cloud resources
are created automatically by this repository.

## API

- `POST /opportunities` creates an opportunity and its first memory event.
- `POST /opportunities/{id}/events` appends a review, progress, or blocker event.
- `GET /opportunities/{id}/memory` returns the complete durable timeline.
- `GET /actions` ranks the next actions using deadline, status, and confidence.
- `GET /actions/brief` asks Gemini for an evidence-grounded Markdown action brief.
- `POST /opportunities/{id}/executions/evidence-check` creates a bounded,
  deterministic verification plan. Separate approval and run endpoints enforce
  a visible plan → human approval → execution → verification → memory loop.
- `GET /health` reports service and database health.

The included execution adapter hashes evidence text immediately, persists only
its digest and byte count, and verifies it against an expected SHA-256 digest.
It is intentionally narrow: a planned action cannot run before
explicit approval, a mismatch fails closed and blocks the opportunity, and the
result is appended to the immutable timeline. This demonstrates the control
plane required for future external adapters without pretending that the demo
can submit entries, spend money, or cross account boundaries.

The Gemini integration receives only the ten highest-ranked opportunity records
and is instructed not to invent eligibility, progress, or rewards. Set
`GEMINI_API_KEY`; `GEMINI_MODEL` defaults to `gemini-2.5-flash`.

## Tests

Run `pytest`.

Every push and pull request also runs the suite on Python 3.11 and 3.12 in
GitHub Actions. The workflow has read-only repository permissions and requires
no cloud credentials, so reviewers can verify the open-source core safely.

See `SUBMISSION_DRAFT.md` for the sponsor mapping, evidence checklist, and the
under-three-minute demo sequence. The draft deliberately leaves cloud and
customer-validation claims unfilled until they can be demonstrated.

`GOAI_SUBMISSION_DRAFT.md` contains the bilingual-review-ready positioning,
open-source evidence, and an honest demo plan for the GOAI preliminary round.
`GOAI_PLATFORM_FIELDS.md` provides copy-ready non-sensitive platform fields, while
`GOAI_DEMO_SCRIPT.md` gives a timed, evidence-first recording plan under three minutes.
Run `./make_goai_demo_video.sh` to generate the 1080p Chinese-narrated GOAI overview;
the generated media stays outside version control, while the script, real dashboard
capture, and narration remain reproducible and reviewable. Run
`./make_goai_submission_package.sh` after committing to create a focused archive
whose manifest binds the source commit, tests, PDF, and video hashes.

Run `./make_devpost_demo_video.sh` to generate the English-narrated, 1080p
CockroachDB × AWS overview. The video explicitly distinguishes reproducible local
evidence from cloud deployment claims that still require independent verification.
The [rendered two-minute demo](assets/opportunity-memory-agent-devpost-1080p.mp4)
is included for reviewers and can be downloaded directly from GitHub.
See [DEVPOST_EVIDENCE.md](DEVPOST_EVIDENCE.md) for the public URLs, checksums,
CI run, and explicit claims boundary.

## License

MIT
