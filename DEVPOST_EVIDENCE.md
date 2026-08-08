# Devpost evidence manifest

Verified on 2026-08-05.

## Public evidence

- Repository: `https://github.com/ILoveBuns/opportunity-memory-agent`
- Public source commit: `0c9d6c3` (Gemini request security, response handling,
  deployment guidance, and evidence boundaries)
- CI workflow: `https://github.com/ILoveBuns/opportunity-memory-agent/actions/workflows/tests.yml`
- Narrated demo: `https://github.com/ILoveBuns/opportunity-memory-agent/raw/main/assets/opportunity-memory-agent-devpost-1080p.mp4`
- Cover image: `https://raw.githubusercontent.com/ILoveBuns/opportunity-memory-agent/main/assets/opportunity-memory-agent-cover.png`
- Current commit tests: 15/15 passed locally on 2026-08-08. GitHub Actions runs
  the same complete `python -m pytest -q` suite on Python 3.11 and 3.12.

## Artifact integrity

```text
3b1764b741ff9dfc13ba6080af50fb229fcbc090a88772c98db694e8d68b3bdb  assets/opportunity-memory-agent-devpost-1080p.mp4
a1d5a20728ca478864af0d8540cd03dfe1adc96b1f21aff1ff68dccc48b6c058  assets/opportunity-memory-agent-cover.png
```

## Claims boundary

- The video is a narrated product overview generated from repository evidence;
  it does not represent an unrecorded live cloud deployment.
- App Runner and CockroachDB Cloud deployment remain pending until account-specific
  resources and secrets are provided and the resulting URL is verified.
- Cloud Run deployment also remains pending. `CLOUD_RUN_DEPLOYMENT.md` provides
  an evidence-first path, but its checklist must not be marked complete until a
  real Google Cloud service, health response, persistent timeline, and Gemini
  request have been verified.
- The project does not claim customers, revenue, awards, or a competition score.
- Identity, legal terms, payments, and account verification remain the entrant's
  responsibility.
