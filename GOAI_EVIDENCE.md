# GOAI submission evidence

Verified through the successful third preliminary submission on 2026-08-05.

## Reproducibility

- Public repository: `https://github.com/ILoveBuns/opportunity-memory-agent`
- Exact source commit: recorded by `GOAI_PACKAGE_MANIFEST.txt` inside the generated ZIP
- Automated tests: `10 passed` with `PYTHONPATH=.:.deps .deps/bin/pytest -q`
- Proposal: `GOAI_PROPOSAL.pdf`
- Narrated demo: `goai-demo-output/opportunity-memory-agent-goai-1080p.mp4`
- Product evidence: the video includes a shared-Chromium capture of the real dashboard and ranked API result, visibly labelled as synthetic in-memory demo data

## Artifact integrity

```text
0e817bd24f7eb0dc054af9fe5262adceb6b5522291219abe9cbd066e78e8551f  GOAI_PROPOSAL.pdf
1d23c4bad2f542200da0c0ce4b5707eff1e69d8575ca0b52f52088872eba2779  goai-demo-output/opportunity-memory-agent-goai-1080p.mp4
```

## Claims boundary

- The test result verifies application behavior covered by the repository tests; it is not a competition score.
- The project does not claim revenue, customers, awards, or a live cloud deployment.
- Identity, legal terms, payment details, and any on-site participation commitment remain for the entrant to confirm.

## Platform evidence

- Registration is complete for the Boundless Agents track.
- Initial submission: `机会记忆智能体`, 2026-08-02 01:29:21, 8.0 MB, under review.
- Organizer notice dated 2026-08-03 requests re-upload of locally retained original ZIP files because some platform-stored attachments were corrupted.
- Submission counter is 1/3; the latest successful submission before the deadline becomes the judging version.
- Re-upload instructions and acceptance criteria are recorded in `GOAI_REUPLOAD_GUIDE.md`.
- On 2026-08-04 the second submission form was prepared with the project name,
  public repository URL, and the verified 4,320,499-byte ZIP. The form remains
  open before submission because the platform requires the entrant's real
  recipient name, phone number, detailed address, and shirt size; none were
  inferred or copied from unrelated sources.
- After the entrant completed the required personal fields, the verified local
  ZIP was submitted successfully. The platform counter changed to `2/3`; the
  new judging record is `机会记忆智能体`, second submission, displayed size
  4.1 MB, timestamp `2026/8/4 21:27:01`, status `审核中`, and the platform
  displayed its explicit success confirmation dialog.

## Closed-loop revision prepared after the second submission

- Added a real approval-gated execution flow: plan, explicit approval,
  deterministic SHA-256 verification, fail-closed state transition, and
  immutable result write-back.
- Evidence text is hashed immediately and is not persisted; only its digest and
  byte count enter the execution record.
- Validation now passes 12/12 automated tests, including approval enforcement,
  successful verification, mismatch handling, and memory write-back.
- Revised proposal PDF SHA-256:
  `d3cd8aa6261b90bd906cebfab8c17ef31c9e6e06282d344d8e75205a98d3e992`.
- Revised 127.637-second 1080p H.264/AAC demo SHA-256:
  `2bb60fefa8e5a07042a9b3b3d83ec19c12602eb4ee67816a6c8f2322a33996f2`.
- Exact source commit: `f1390068e979534cedf52c7d2caf014c79a8837a`.
- Final package SHA-256:
  `b83ca83ec41cfd005ccf9bb9ae6721e610b3bf266f34f69cec0dee92286e0eb2`
  (4,345,208 bytes).
- The platform's legacy enrollment record had no topic. The correct workflow
  was to select the topic in the preliminary submission form itself. The third
  submission succeeded on 2026-08-05 at 09:30:51 UTC+8 and is now the judging
  version: attempt 3/3, status `submitted` / `审核中`, topic key
  `ai_finance` (`赛题三：AI+金融`), and total size 4,345,208 bytes. The API
  returned HTTP 201 for draft creation, upload init, upload part, upload
  completion, and final submission; a subsequent read-only record fetch
  confirmed `isReviewVersion: true`.
