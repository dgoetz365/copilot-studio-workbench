# Design decisions

## A bounded tool is easier to reason about

The contract exposes a single GET operation with a short query string. It cannot send a message, execute code, read arbitrary files, or mutate a job. The server uses fixed synthetic fixtures and does not accept a user-selected data source. This keeps authority independent of conversational wording.

## Unknown and ambiguous are ordinary outcomes

HTTP 200 means the lookup completed, not that it found a record. `outcome` distinguishes found, ambiguous, and not found. Invalid requests use HTTP 400. A cloud transport failure follows the topic's error path and must not be converted into an ordinary missing record.

Only a unique match has a source ID and job fields. A partial job number never falls back to a similar title. Title search uses all query words and returns candidate IDs when more than one record matches. These are simple deterministic rules, not a claim of intelligent semantic search.

## Generate display text from the same record

The API constructs its message from the verified match. The sample topic displays that message directly; it does not ask a model to infer a collection date or rewrite a status. Missing dates remain explicit. This trades conversational flexibility for a small and testable evidence boundary.

## Approval text does not authorize a write

The second topic previews a proposed change and asks whether the draft reflects the user's intent. It never labels the job changed. The API has no write operation. Moving to actual execution would require a separate design and server-side authorization; adding an optimistic confirmation message would not be sufficient.

## Platform syntax is not platform execution

YAML syntax, OpenAPI schema checks, local API tests, tenant import, tool authentication, topic routing, and live runtime behavior are different checks. This repository records the first group and leaves the tenant/runtime group explicitly unverified. No environment identifiers or connection references are invented to make the examples appear deployed.

## New public example

The print-desk scenario, records, code, and topics were created for this repository. The example demonstrates general assistant engineering patterns without copying an employer agent, prompt collection, source system, or conversation history.
