# Copilot Studio Workbench

An inspectable example of the engineering around a Copilot Studio assistant: explicit conversation topics, a read-only API contract, evidence-bearing responses, ambiguous-match handling, and a human review step. The fictional scenario is a community print desk with three invented jobs.

This repository contains **working local software and original configuration examples**. The Python API and reference cases run without a cloud account. The Copilot Studio topics and connector definition are integration starting points; they have not been imported into or executed in a tenant. No employer source, topics, connections, documents, identities, or data are included.

## Run locally

From the repository root with Python 3.12 or newer:

```sh
python app.py lookup "garden club"
python app.py evaluate
python app.py serve
```

There are no runtime dependencies. The first command returns an ambiguous result with two candidate IDs, without choosing a job. Try `python app.py lookup JOB-101` for a source-backed status with an explicitly unconfirmed collection time. `evaluate` runs eight deterministic reference cases; it does **not** run a language model or Copilot Studio.

The server listens only at `http://127.0.0.1:8767`. Query it with `curl "http://127.0.0.1:8767/lookup?query=JOB-102"`. Stop with Ctrl+C. Use `--port 8768` if needed. Nothing opens a browser, writes business data, or contacts another service.

## What is here

| Artifact | Purpose |
| --- | --- |
| [app.py](app.py) | Runnable lookup API, CLI, and reference-case evaluator |
| [Print-status topic](topics/print-status.topic.yaml) | Collect a query, call an HTTP tool, and display the evidence-bearing result |
| [Change-request topic](topics/change-request.topic.yaml) | Collect a proposed change, preview it, and branch on human confirmation without claiming a write |
| [Connector definition](connector/print-desk.swagger.json) | OpenAPI 2.0 contract with one read-only operation and typed outcomes |
| [Reference cases](evaluation/cases.json) | Exact, ambiguous, unknown, incomplete-ID, and instruction-like queries |
| [Integration notes](docs/integration.md) | Deliberate steps and acceptance checks for a separate Copilot Studio test environment |
| [Design decisions](docs/decisions.md) | Why evidence, transport, and conversational approval have different responsibilities |

The HTTP topic and the custom connector are **alternative integration routes**. The topic does not contain an environment-specific connector binding. Both describe the same `/lookup` contract.

```mermaid
flowchart LR
  Q[Topic asks for query] --> T[HTTP action or configured connector]
  T --> API[Read-only lookup API]
  API --> R[Found / ambiguous / not found]
  R --> M[Deterministic message and source ID]
  M --> Q
```

The checked-in host `api.example.invalid` is intentionally nonfunctional. The local server is not publicly hosted and cannot be called directly by a cloud agent. [Integration notes](docs/integration.md) explain the remaining deployment, authentication, and tenant-validation work.

## Evidence and limits

The API emits a source ID only after finding exactly one record. An ambiguous result contains candidates and asks for an exact ID; a missing date remains unconfirmed. No semantic claim is delegated to a model in this sample. Input text cannot introduce additional tools or change a record.

The change-request topic demonstrates conversational review, not authorization or persistence. A “yes” response does not execute an operation. The topic explicitly says that nothing was saved or sent. A real write tool would need its own identity, authorization, fresh-state checks, idempotency, and execution receipt.

Run `python -m unittest discover -s tests -v` for behavioral and real local HTTP tests. See [VALIDATION.md](VALIDATION.md) for executed checks and the distinction between syntax, API behavior, and tenant/runtime proof.

Licensed under [MIT](LICENSE). All fixtures and configuration are newly written for this public example.
