# AWS App Runner deployment

The repository includes `apprunner.yaml` so the API can be deployed from the
GitHub source repository without maintaining a separate container registry.

## Prerequisites

- A CockroachDB Cloud connection string with `sslmode=verify-full`.
- Two AWS Secrets Manager secrets named `OPPORTUNITY_MEMORY_DATABASE_URL` and
  `OPPORTUNITY_MEMORY_GEMINI_API_KEY`.
- An App Runner instance role allowed to read only those two secrets.

## Deploy

1. In AWS App Runner, create a source-code service from this repository and
   branch.
2. Select **Use a configuration file**; App Runner reads `apprunner.yaml`.
3. In the service configuration, map `DATABASE_URL` and `GEMINI_API_KEY` to
   their full Secrets Manager ARNs, then attach the narrow instance role. Secret
   ARNs are account-specific and therefore deliberately not checked in.
4. Deploy and wait for `/health` to return
   `{"status":"ok","database":"connected"}`.
5. Run `python scripts/seed_demo.py` once with the production `DATABASE_URL`,
   then exercise the dashboard and memory timeline.

The startup command applies the idempotent schema before serving requests.
Credentials are referenced by secret name and are never stored in the
repository or App Runner configuration file.

## Evidence checklist

- Capture the App Runner service URL and successful `/health` response.
- Capture the CockroachDB Cloud tables and append-only memory rows.
- Create an opportunity, append a blocker, restart/redeploy the API, and show
  that the timeline persists.
- Generate a Gemini brief and compare every statement with the ranked records.
