# Gemini XPRIZE Devpost form worksheet

Verified against the repository and the live Devpost form on 2026-08-05.
This worksheet separates evidence-backed copy from entrant attestations. Do not
paste an item marked `CONFIRM` until the entrant has verified it.

## Current submission state

- Devpost project: `Opportunity Memory Agent`
- Status: `DRAFT`, 3/5 steps complete
- Repository: `https://github.com/ILoveBuns/opportunity-memory-agent`
- First repository commit: 2026-08-01 (`bd56edd`)
- Current public evidence commit: `0c9d6c3`
- Public project page: `https://devpost.com/software/opportunity-memory-agent`

## Recommended category

`Professional Services Access`

Rationale: the product helps people and small teams navigate grants,
competitions, compliance tasks, sales leads, and other professional opportunity
workflows. `Small Business Services` is a reasonable alternative if the entrant
wants to position the product primarily as a B2B operations tool.

## Evidence-backed answers

### Project start date

`08-01-26`

Evidence: the first Git commit is dated 2026-08-01. `CONFIRM` that no materially
equivalent private or pre-repository version existed before this date.

### How the project uses AI to impact the world

Opportunity Memory Agent helps individuals and small teams pursue grants,
competitions, compliance tasks, and commercial opportunities without losing
critical context. It stores an append-only timeline of deadlines, reviews,
progress, and blockers; ranks the next actions deterministically; and uses
Gemini to turn only the highest-ranked, evidence-backed records into a concise
execution brief. This design makes AI assistance more accountable: the model is
explicitly instructed not to invent eligibility, completion, rewards, or other
facts that are absent from the durable record.

### Underlying business model

The intended model is a subscription software service for individuals and small
teams managing high-value opportunity pipelines. A free tier would support a
limited number of active opportunities and local/self-hosted evaluation. Paid
plans would add shared workspaces, managed durable storage, integrations,
scheduled evidence checks, configurable retention, and higher Gemini usage.
The current hackathon project is an open-source prototype and has not generated
revenue.

### How operations can be sustained

The open-source core keeps adoption and independent verification inexpensive.
A managed service can fund hosting, database operations, model usage, support,
and integration maintenance through recurring individual and team
subscriptions. Deterministic ranking and bounded model context limit inference
costs, while usage caps and metering keep free and paid tiers economically
predictable. This is a planned model, not evidence of an existing commercial
operation.

### Why the model is sustainable and viable

Users receive value when one prevented missed deadline or recovered follow-up
is worth more than the subscription price. The product stores structured facts
and calls Gemini only for a bounded top-ten brief, which limits variable cost.
The same core can serve multiple professional workflows without maintaining a
separate model for each vertical. Viability has not yet been validated with
paying customers, so the submission should describe this as a testable business
hypothesis rather than proven traction.

### How the business operates with AI

Deterministic code stores and ranks the opportunity records. Gemini receives a
bounded representation of the ten highest-ranked actions and produces a
grounded execution brief. The prompt requires the model to preserve blockers
and avoid inventing progress, eligibility, or rewards. AI therefore improves
the readability and usability of an auditable workflow without replacing the
system of record or silently deciding that an external action has occurred.

### Extent to which AI is live in production

The Gemini integration is implemented and covered by automated request/response
tests, but the project is not represented as a production deployment. The
public demo supports a zero-credential synthetic path, while a real Gemini call
requires `GEMINI_API_KEY`. No claim should be made that Gemini is serving real
customers or making production decisions until a live deployment and call have
been independently verified.

### AI tools used

- Gemini API, default model configuration `gemini-2.5-flash`, for grounded
  action-brief generation.
- Deterministic Python scoring for priority ordering; it is deliberately kept
  separate from the LLM.
- `CONFIRM` any additional development assistants that the entrant must disclose
  under the rules.

### LLM and Gemini API usage

The application sends a bounded prompt containing at most the ten
highest-ranked opportunity records to the Gemini `generateContent` endpoint.
The prompt tells Gemini to treat record values as untrusted data, preserve
unresolved blockers, and never invent eligibility, completion, or rewards. The
API key is transmitted in the documented `x-goog-api-key` header rather than in
the URL. The response becomes a human-readable action brief; durable state and
priority scores remain governed by the database and deterministic code. The
model is configured through `GEMINI_MODEL`, which defaults to
`gemini-2.5-flash`.

### Repository URL

`https://github.com/ILoveBuns/opportunity-memory-agent`

The repository is public. `CONFIRM` the Devpost checkbox about access for
`testing@devpost.com` and `judging@hacker.fund`; this is an entrant attestation.

### Pre-existing resources

Evidence currently supports: `None; the repository's first commit is dated
August 1, 2026.`

`CONFIRM` that no code, business, customer list, dataset, brand, or other project
resource existed before May 19, 2026.

## Google Cloud evidence gap

The repository proves a Gemini REST integration, Docker Compose deployment, and
an AWS App Runner deployment template. It does **not** currently prove a Google
Cloud project, Google Cloud deployment, Vertex AI use, or a real Gemini API call.

Do not answer the Google Cloud product question by claiming Vertex AI, Cloud Run,
or another service unless it is actually provisioned and verified. The minimum
credible path is:

1. Create or select a Google Cloud project under the entrant's account.
2. Enable an applicable Gemini/Vertex AI API and authenticate without committing
   credentials.
3. Run one real, bounded brief request and preserve a redacted response plus
   project/service evidence.
4. Optionally deploy the container to Cloud Run with managed secrets and verify
   `/health` and the dashboard.
5. Update the repository evidence manifest with only non-sensitive project,
   service, commit, and verification details.

These account, billing, terms, and credential actions require entrant approval.

## Financial and traction fields — entrant confirmation required

Repository evidence supports no customers, revenue, production deployment, or
paid acquisition. If accurate, the likely entries are:

- Total revenue: `$0`
- Revenue by month: `May $0; June $0; July $0; August $0`
- Related-party revenue: `$0`
- Users acquired: `0`
- Paying users: `0`
- Customer testimonial: leave blank

`CONFIRM` every value. Expenses and cost of goods sold cannot be inferred from
the repository. Include any real cloud, API, domain, software, contractor,
advertising, or other costs incurred during the hackathon period; do not default
them to zero without checking.

## Other entrant decisions

- Submitter type: `CONFIRM` Individual / Team / Organization.
- Country or countries represented: `CONFIRM`.
- Learning level: `CONFIRM`; `Significant` is plausible but is a subjective
  entrant statement.
- Agentic Economy Prize: do not opt in without a real Circle wallet transaction,
  public integration repository, and block-explorer proof.
- Final rules/terms checkbox and submission action: entrant must review and
  confirm.
