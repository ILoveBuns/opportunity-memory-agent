# Submission draft

## Project name

Opportunity Memory Agent

## One-line pitch

A durable operations agent that remembers every deadline, review, blocker, and
next action, then uses deterministic ranking plus Gemini to produce a grounded
execution brief.

## Problem

People pursuing grants, competitions, sales leads, or compliance tasks lose
context across weeks of email and organizer review. Stateless assistants repeat
work, miss changed deadlines, and hallucinate progress.

## Solution

The service stores an append-only event timeline in CockroachDB. Every status
change remains auditable. A deterministic scorer ranks actionable work using
deadline, reward, confidence, and blocker state. Gemini receives only the ten
highest-ranked database records and turns them into a concise action brief with
an explicit instruction not to invent progress or eligibility.

## Sponsor technology

- CockroachDB is the system of record for opportunities and immutable memory
  events.
- The API is packaged for deployment to AWS App Runner or ECS.
- `apprunner.yaml` provides a reproducible source deployment; the deployment
  guide maps CockroachDB/Gemini credentials through AWS Secrets Manager.
- Gemini generates the human-readable operations brief from bounded facts.

## Demo sequence (under three minutes)

1. Open `/` and create an opportunity in the responsive dashboard, then show its initial memory event.
2. Append a progress event, then a blocker event.
3. Retrieve the complete chronological memory timeline.
4. Open `/actions` and show deterministic reprioritization.
5. Open `/actions/brief` and show Gemini's grounded top actions and blockers.
6. Restart the API and retrieve the same timeline to demonstrate persistence.

## Evidence still required before submission

- Public AWS deployment URL and CockroachDB Cloud connection.
- Screen recording of the deployed flow.
- Exact Devpost track selections and accepted rules.
- Gemini/Google Cloud project evidence for the XPRIZE submission.
- Truthful customer or revenue validation if required by the XPRIZE rules.
