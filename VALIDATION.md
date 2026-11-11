# Validation

Verified on 2026-11-11 with Python 3.12.14.

| Check | Result |
| --- | --- |
| `python -m unittest discover -s tests -v` | 11 tests passed, including real loopback HTTP and a CLI subprocess |
| `python app.py evaluate` | Eight reference cases passed; API behavior only |
| Both topic files parsed with PyYAML 6.0.3 | Valid YAML and unique node IDs within each topic |
| Connector parsed with openapi-spec-validator 0.9.0 | Valid OpenAPI 2.0 document |
| All eight reference responses checked with jsonschema 4.26.0 | Match the declared response schema |

The three schema-validation packages were used as external development tools; they are not required to run the API, CLI, or tests. A valid YAML document is not proof of a valid Copilot Studio topic. OpenAPI validation is not proof of successful connector import, configured credentials, tool execution, or platform-policy compatibility.

No tenant was accessed. No topic or connector was imported, published, or called in Copilot Studio. The intentionally invalid host was not replaced. No browser, language model, live business system, or cloud endpoint was used for runtime verification. Follow the separate integration acceptance checks before treating this as a running cloud agent.

The local tests cover exact and ambiguous matches, unknown identifiers, empty and malformed input, instruction-like input treated as data, response isolation from fixture mutation, query validation, host checks, read-only routing, and absence of arbitrary file serving. They do not establish production security, load capacity, conversational intent accuracy, or human-review effectiveness.
