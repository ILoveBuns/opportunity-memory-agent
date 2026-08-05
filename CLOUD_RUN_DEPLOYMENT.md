# Google Cloud Run deployment and evidence checklist

This is an evidence-first deployment path for the Gemini XPRIZE submission. It
does not claim that a Google Cloud project, billing account, Cloud Run service,
production database, or Gemini credential already exists.

The official references are:

- Cloud Run deployment: https://docs.cloud.google.com/run/docs/deploying
- Cloud Run secrets: https://docs.cloud.google.com/run/docs/configuring/services/secrets

The current application uses the Gemini Developer API with an API key. It does
not claim Vertex AI. If the entrant later chooses Vertex AI, update the code and
evidence against the then-current Google Cloud documentation instead of treating
the existing API-key integration as Vertex AI usage.

Creating a project, enabling billing or APIs, accepting terms, assigning IAM,
and creating secrets are account actions for the entrant. Never commit secret
values, access tokens, project credentials, or database connection strings.

## Required account decisions

Before running commands, the entrant must choose and verify:

- `PROJECT_ID`: a Google Cloud project controlled by the entrant;
- `REGION`: a Cloud Run region available to that project;
- whether the service may be public during judging;
- a dedicated runtime service account with least privilege;
- a reachable PostgreSQL-compatible `DATABASE_URL` with TLS;
- a real Gemini credential and the applicable API/terms;
- billing and budget controls.

## One-time service preparation

The exact IAM grants depend on the account. The deployer needs the Cloud Run,
build, Artifact Registry, and service-account permissions required by Google's
current documentation. The runtime identity should receive only Secret Manager
access to the two secrets used by this service.

Create two Secret Manager secrets through the console or the entrant's approved
workflow:

- `opportunity-memory-database-url`
- `opportunity-memory-gemini-api-key`

Store the values as secret versions. Do not place them in shell history or this
repository.

## Deploy from source

After authenticating `gcloud` to the approved project, run from the repository
root. Replace every bracketed value before execution.

```bash
gcloud run deploy opportunity-memory-agent \
  --source . \
  --project [PROJECT_ID] \
  --region [REGION] \
  --port 8000 \
  --service-account [RUNTIME_SERVICE_ACCOUNT] \
  --set-secrets DATABASE_URL=opportunity-memory-database-url:latest,GEMINI_API_KEY=opportunity-memory-gemini-api-key:latest \
  --set-env-vars GEMINI_MODEL=gemini-2.5-flash \
  --max-instances 2 \
  --no-allow-unauthenticated
```

Start private. If the entrant explicitly chooses a public judging URL and the
project policy permits it, change access through Cloud Run IAM rather than
embedding credentials in a URL or repository file.

## Verification sequence

Record only non-sensitive evidence.

1. Capture the source commit and Cloud Run revision name.
2. Request `/health`; require `status=ok` and `database=connected`.
3. Create one synthetic opportunity through the dashboard.
4. Append a progress event and a blocker event.
5. Record the timeline response and ranked actions with synthetic data only.
6. Request `/actions/brief` once and verify every Gemini statement against the
   ranked records.
7. Redeploy or restart the service, then retrieve the same timeline to prove
   persistence.
8. Capture a redacted Cloud Run service/revision view and a redacted API usage
   view that identify the project and product but expose no credential or user
   data.
9. Record resource cleanup or the budget/scale limits that keep the service
   bounded after judging.

## Evidence record template

Do not fill an item until it has been observed.

```text
Source commit:
Google Cloud project (non-sensitive ID only):
Cloud Run region:
Cloud Run service:
Cloud Run revision:
Deployment time:
Health verification time and result:
Persistence verification time and result:
Gemini model and verified request time:
Redacted evidence URLs or artifact hashes:
Cleanup/budget status:
```

## Claims boundary

Until every verification item is complete, submission materials may say that
the repository is Cloud Run-ready and contains a documented deployment path.
They must not say that the service is deployed, in production, serving users,
using Vertex AI, or backed by a live Google Cloud project.
