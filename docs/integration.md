# Connecting the example in a separate test environment

These steps are a review plan. No connector, topic, authentication configuration, or agent has been created or published by this repository.

## Choose an integration route

**HTTP topic:** create a blank topic, inspect [print-status.topic.yaml](../topics/print-status.topic.yaml), and adapt it in the topic code editor. Replace the invalid URL with an API you control. Configure credentials outside the checked-in YAML. Review the generated response type in the authoring canvas and test it before publication. The sample uses the HTTP node's default error path; configure and test the agent's On Error topic so transport failures never look like missing records. Microsoft documents the [HTTP node, response types, error behavior, and timeout settings](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-http-node).

**Custom connector:** import [print-desk.swagger.json](../connector/print-desk.swagger.json) into a test solution, replace the invalid host, configure authentication, and create a test connection. Add its `LookupPrintJob` operation as a tool or select it in a topic through the authoring canvas. This produces tenant-specific bindings that are intentionally absent here. Microsoft documents [OpenAPI 2.0 connector import](https://learn.microsoft.com/en-us/connectors/custom-connectors/define-openapi-definition) and [connector tools in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors).

The local Python development server is only a contract test target. A cloud integration requires an appropriately hosted, authenticated implementation of the contract. Do not expose this local server or mistake its Host check for user authorization. No hosting or connection setup is automated here.

## Validate inside the tenant

1. Confirm the topic and connector save without platform errors. YAML parsing and OpenAPI validation alone do not establish this.
2. Test `JOB-101`, `JOB-102`, `garden club`, `JOB-999`, and a title query. Compare the returned source IDs, unknown values, and ambiguous outcomes against the local reference cases.
3. Disconnect or fail the API deliberately. Verify the error path reports unavailable evidence, rather than a fabricated status or “no match.”
4. Test a follow-up exact ID after an ambiguous result. Verify your chosen topic routing and variable scope preserve the intended context.
5. Try the separate change-request topic with both yes and no. Confirm that no record is written and the text accurately describes that boundary.
6. Inspect actual tool traces and authentication before separately deciding whether to publish the test agent.

The topic structure follows Microsoft's [topic component documentation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/visual-studio-code-extension-edit-agent-components). Current environment capabilities and authoring validation must be checked in the intended tenant.
