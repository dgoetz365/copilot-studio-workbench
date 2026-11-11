# Copilot Studio Workbench

Build a conversation around explicit evidence: original Copilot Studio topics, a connector contract, and a working lookup API for a fictional print desk.

**Python 3.12+ · Copilot Studio YAML · OpenAPI 2.0 · No Python runtime dependencies**

[Full guide](docs/guide.md) · [Portfolio](https://github.com/dgoetz365) · [MIT license](LICENSE)

**Status:** the local API and reference cases are tested. Copilot Studio tenant import and runtime are unverified.

## Quick start

```sh
git clone https://github.com/dgoetz365/copilot-studio-workbench.git
cd copilot-studio-workbench
python app.py lookup "garden club"
python app.py evaluate
```

The lookup returns two candidate jobs instead of guessing. The evaluator runs eight deterministic API reference cases; it does not run a model or a Copilot Studio agent.

On Windows, `py -3.12` can replace `python`. If you already cloned the repo, start with the Python commands from its root.

## Try it

Run `python app.py lookup JOB-101` for a source-backed status with an explicitly unconfirmed collection time. Run `python app.py serve` to expose the same lookup at `http://127.0.0.1:8767/lookup?query=JOB-101` on your computer.

## Engineering highlights

- **Explicit outcomes:** found, ambiguous, and missing results have defined response shapes and evidence fields.
- **Conversation design:** one topic retrieves status; another previews a proposed change for human review without claiming a write.
- **Integration choices:** an HTTP topic and a custom connector demonstrate alternative routes to the same read-only contract.

[Topic definitions](topics/) · [Connector](connector/print-desk.swagger.json) · [Reference cases](evaluation/cases.json) · [Integration guide](docs/integration.md) · [Validation](VALIDATION.md)

## Tests and scope

```sh
python -m unittest discover -s tests -v
```

All code, configuration, and records are original synthetic examples. The placeholder host is intentionally nonfunctional. Cloud access requires separate deployment, authentication, and tenant validation; the local server has no production access controls.

Built by [Daniel Goetz](https://github.com/dgoetz365) as an independent portfolio example. Employer code and data are not included.
