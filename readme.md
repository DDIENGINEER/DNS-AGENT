# DNS Agent -- AI-Powered DNS Lookup Assistant

## 1. Project Overview

The **DNS Agent** is a Python-based, AI-assisted DNS lookup and
validation application. It uses an OpenAI model with tool/function
calling to answer DNS questions by invoking a controlled set of Python
tools.

The current implementation uses fictional JSON datasets to simulate DNS
infrastructure. The project is being developed incrementally, with
FastAPI, enterprise authentication, Microsoft Teams integration, and
real DNS/DDI integrations planned for later phases.

### Current objective

Build a read-only DNS assistant that can:

-   Search private DNS records.
-   Search public DNS records.
-   Compare DNS responses across regions.
-   Identify the hosting platform for a DNS zone.
-   Explain findings in natural language while grounding answers in tool
    results.

> **Important:** The current datasets are mock data. The assistant is
> not yet connected to production DNS servers or EfficientIP.

------------------------------------------------------------------------

## 2. Business Use Case

DNS operations teams regularly investigate questions such as:

-   Does a hostname exist in private DNS or public DNS?
-   What record type and value are configured?
-   Does the hostname resolve consistently across regions?
-   Which platform hosts the DNS zone?
-   Are there differences between regional responses that need
    investigation?

The DNS Agent aims to reduce manual lookups and consolidate results from
multiple sources into a single operational response.

The longer-term goal is to provide a controlled conversational interface
for DNS operations, potentially through Microsoft Teams.

------------------------------------------------------------------------

## 3. Project Requirements

### 3.1 Functional requirements

  -----------------------------------------------------------------------
  ID                      Requirement             Status
  ----------------------- ----------------------- -----------------------
  FR-01                   Accept a DNS question   Implemented in CLI test
                          in natural language     

  FR-02                   Search private DNS      Implemented using mock
                          records by hostname     JSON

  FR-03                   Search public DNS       Implemented using mock
                          records by hostname     JSON

  FR-04                   Validate DNS responses  Implemented using mock
                          across configured       JSON
                          regions                 

  FR-05                   Identify DNS zone       Implemented using mock
                          hosting platform        JSON

  FR-06                   Combine tool results    Implemented
                          into a natural-language 
                          response                

  FR-07                   Expose the assistant    Planned
                          through a REST API      

  FR-08                   Integrate the assistant Planned
                          with Microsoft Teams    

  FR-09                   Connect to approved     Planned
                          live DNS/DDI data       
                          sources                 
  -----------------------------------------------------------------------

### 3.2 Non-functional requirements

-   **Security:** Secrets must not be hardcoded or committed to source
    control.
-   **Read-only operation:** The initial release must not modify DNS
    records or infrastructure.
-   **Traceability:** Tool execution and operational requests should be
    auditable before production use.
-   **Reliability:** Tool failures must be handled without silently
    inventing results.
-   **Maintainability:** Keep the agent, tools, configuration, and API
    layers separate.
-   **Extensibility:** New data sources and tools should be added
    through controlled interfaces.
-   **Validation:** Inputs and tool outputs must be validated before
    use.
-   **Least privilege:** Future integrations must use service identities
    with only the permissions required.

------------------------------------------------------------------------

## 4. Technology Stack

  -----------------------------------------------------------------------
  Component               Technology              Purpose
  ----------------------- ----------------------- -----------------------
  Language                Python                  Application and tool
                                                  implementation

  AI model                OpenAI API              Natural-language
                                                  reasoning and response
                                                  generation

  SDK                     OpenAI Python SDK       Model and tool-calling
                                                  integration

  Tool interface          Function/tool calling   Lets the model request
                                                  approved Python
                                                  functions

  Configuration           python-dotenv           Loads local environment
                                                  variables

  Current data source     JSON files              Mock DNS and hosting
                                                  datasets

  API layer               FastAPI                 Planned REST interface

  ASGI server             Uvicorn                 Planned API runtime

  Data validation         Pydantic                Planned
                                                  request/response
                                                  validation

  IDE                     Visual Studio Code      Development environment
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 5. Current Project Structure

The current project is organised as follows. Some future files are shown
as planned and may not exist yet.

``` text
DNS AGENT/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── tools.py
│   ├── agent.py
│   └── main.py                 # Planned: FastAPI entry point
│
├── data/
│   ├── private_dns.json
│   ├── public_dns.json
│   ├── regional_resolution.json
│   └── hosting_inventory.json
│
├── venv/                       # Local virtual environment; do not commit
├── .env                        # Local secrets; do not commit
├── .gitignore
├── test_tools.py
├── test_agent.py
├── requirements.txt            # Add/maintain as dependency list
└── README.md
```

### File responsibilities

  -----------------------------------------------------------------------
  File                                Responsibility
  ----------------------------------- -----------------------------------
  `app/config.py`                     Loads environment variables and
                                      model configuration

  `app/tools.py`                      Reads mock datasets and exposes DNS
                                      lookup functions

  `app/agent.py`                      Defines the system instructions,
                                      tool schemas, tool execution and
                                      model loop

  `data/*.json`                       Holds fictional DNS, regional
                                      resolution and hosting inventory
                                      data

  `test_tools.py`                     Tests the Python data lookup
                                      functions

  `test_agent.py`                     Runs an end-to-end question through
                                      the AI agent

  `app/main.py`                       Planned FastAPI application entry
                                      point
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 6. Current Architecture

``` text
                 User question
                       |
                       v
              test_agent.py (CLI)
                       |
                       v
                 app/agent.py
             OpenAI Responses API
                       |
             Model selects a tool
                       |
                       v
                Tool allowlist
                       |
                       v
                 app/tools.py
                       |
          +------------+-------------+
          |            |             |
          v            v             v
      Private DNS   Public DNS   Regional DNS
          |            |             |
          +------------+-------------+
                       |
                       v
              Hosting inventory
                       |
                       v
                JSON mock data
                       |
                       v
             Tool results returned
                       |
                       v
              AI-generated summary
                       |
                       v
                  User response
```

### Request execution flow

1.  The user submits a natural-language DNS question.
2.  `agent.py` sends the question, system instructions and approved tool
    definitions to the OpenAI API.
3.  The model may request one or more tools.
4.  The application checks each requested tool against the local
    allowlist.
5.  The selected Python function reads the relevant JSON dataset.
6.  The application returns the tool output to the model.
7.  The model prepares a consolidated response based on the returned
    data.
8.  The response is displayed to the user.

The model does not directly access the local files. The Python
application controls which functions can be executed.

------------------------------------------------------------------------

## 7. Work Completed

  -----------------------------------------------------------------------
  Area                                Work completed
  ----------------------------------- -----------------------------------
  Development environment             Created the Python virtual
                                      environment and configured it in VS
                                      Code

  Dependencies                        Installed the OpenAI SDK, FastAPI,
                                      Uvicorn, python-dotenv and Pydantic

  Secrets                             Configured `.env` for the OpenAI
                                      API key and model name

  Source control hygiene              Added secret and
                                      virtual-environment exclusions to
                                      `.gitignore`

  Mock datasets                       Created private DNS, public DNS,
                                      regional resolution and hosting
                                      inventory JSON files

  Data access                         Implemented JSON loading and four
                                      DNS lookup functions in
                                      `app/tools.py`

  Tool testing                        Executed `test_tools.py` and
                                      verified the lookup functions

  Agent configuration                 Implemented model configuration and
                                      system instructions

  Tool schemas                        Defined four function tools with
                                      strict JSON parameter schemas

  Tool execution                      Added an allowlisted function
                                      mapping and tool execution loop

  Agent testing                       Executed `test_agent.py`
                                      successfully against the mock
                                      datasets
  -----------------------------------------------------------------------

### Current sample scenario

The current test asks the agent to:

-   Check `api.example.com` in private and public DNS.
-   Validate its response in India, Europe and the US.
-   Identify the hosting platform.
-   Explain any regional differences.

The mock data demonstrates how the agent can consolidate multiple tool
results into one response. The IP addresses and DNS records in this
scenario are illustrative only.

------------------------------------------------------------------------

## 8. Guardrails and Security

Guardrails are controls that constrain what the assistant can access and
do. It is important to distinguish controls already implemented from
controls that are only planned.

### 8.1 Implemented guardrails

  -----------------------------------------------------------------------
  Guardrail               Implementation          Strength / limitation
  ----------------------- ----------------------- -----------------------
  Scope instructions      System prompt defines   Behavioural guidance;
                          the assistant as a DNS  not a security boundary
                          lookup assistant        by itself

  No invented DNS data    Prompt instructs the    Must be reinforced with
                          model to rely on tool   application-side
                          results                 validation

  Tool allowlist          `FUNCTIONS` mapping     Strong application-side
                          exposes only approved   restriction on callable
                          Python functions        functions

  Read-only capability    Current tools only read No DNS modification
                          predefined JSON         function is exposed
                          datasets                

  Tool error handling     Tool execution catches  Production error
                          exceptions and returns  messages should be
                          an error result         sanitised

  Tool iteration limit    Agent loop has a        Limits rounds, but
                          maximum of eight        should also limit total
                          iterations              tool calls

  Secret configuration    API key is loaded from  Key presence is
                          `.env`                  checked; validity and
                                                  rotation are not
                                                  managed

  Dataset boundary        Tools read files from   Dataset access should
                          the project's `data/`   be further constrained
                          directory               as sources expand
  -----------------------------------------------------------------------

### 8.2 Guardrails not yet implemented

The following controls are required before connecting the assistant to
production systems:

-   Strict hostname/FQDN validation and normalisation.
-   Pydantic validation for API requests and tool arguments.
-   Maximum question length and request-size limits.
-   Per-user authentication and role-based access control (RBAC).
-   Authorisation checks for permitted zones, environments and regions.
-   Prompt-injection handling and separation of instructions from
    untrusted data.
-   Tool-level timeouts and bounded retries.
-   Per-request and per-user rate limits.
-   Structured audit logs for user, question, tool, arguments, result
    status and timestamp.
-   Sanitised error messages that do not expose internal paths,
    credentials or infrastructure details.
-   Output validation to ensure the final response does not claim
    unsupported facts.
-   Secure secret storage and rotation for deployed environments.
-   Monitoring, alerting and operational health checks.

### 8.3 Read-only principle

The initial production release should remain read-only.

The AI model must never be given direct credentials or unrestricted
access to DNS/DDI infrastructure. All infrastructure access must happen
through approved application tools, with explicit validation and
authorisation.

Any future write operation must be implemented as a separate workflow
with approval, audit, validation and rollback considerations. It must
not be enabled merely by adding a tool to the agent.

------------------------------------------------------------------------

## 9. Target Architecture

The target architecture separates the user interface, API, agent
orchestration, tools, integrations and security controls.

``` text
                 Microsoft Teams
                        |
                        v
                 Teams Bot / Adapter
                        |
                        v
                  FastAPI Gateway
                        |
          +-------------+--------------+
          |                            |
          v                            v
   Authentication / RBAC        Request validation
          |                            |
          +-------------+--------------+
                        |
                        v
                 Agent Orchestrator
                        |
              Intent and tool selection
                        |
                        v
                 Policy / Guardrail
                        |
                        v
                  Tool Registry
                        |
        +---------------+----------------+
        |               |                |
        v               v                v
   DNS lookup      Regional check    Zone ownership /
   and records     and comparison    hosting lookup
        |               |                |
        +---------------+----------------+
                        |
                        v
               Integration adapters
                        |
       +----------------+-------------------+
       |                |                   |
       v                v                   v
   EfficientIP       BIND / DNS       Approved inventory
   APIs              resolvers        and CMDB sources
                        |
                        v
               Normalised tool results
                        |
                        v
                Response validation
                        |
                        v
                 Audit / telemetry
                        |
                        v
              Response to Teams user
```

### Target architecture principles

1.  **API-first:** The core assistant should be accessible through a
    documented REST API.
2.  **Channel independence:** Teams should be a client of the API, not
    the place where business logic lives.
3.  **Tool-based access:** All infrastructure access must be mediated by
    approved tools.
4.  **Least privilege:** Each integration should have only the
    permissions it requires.
5.  **Policy before execution:** Validate identity, scope, intent and
    parameters before running tools.
6.  **Auditable operations:** Record requests and tool execution
    outcomes.
7.  **Modular integrations:** EfficientIP, BIND and other data sources
    should be implemented behind separate adapters.
8.  **Safe failure:** If a source is unavailable or data is incomplete,
    report that clearly instead of guessing.

------------------------------------------------------------------------

## 10. Future Scope and Phased Roadmap

### Phase 1 -- Complete the local MVP

-   [x] Python project structure
-   [x] Mock DNS datasets
-   [x] Private DNS lookup tool
-   [x] Public DNS lookup tool
-   [x] Regional DNS validation tool
-   [x] Hosting identification tool
-   [x] OpenAI tool-calling integration
-   [x] End-to-end CLI test
-   [ ] Add automated unit tests and test fixtures
-   [ ] Add hostname and tool-argument validation
-   [ ] Add structured application logging
-   [ ] Create and maintain `requirements.txt`

### Phase 2 -- FastAPI service

-   Create `app/main.py`.
-   Implement a health-check endpoint.
-   Implement a DNS assistant query endpoint.
-   Define Pydantic request and response models.
-   Add request validation and consistent error responses.
-   Add API-level logging and request correlation IDs.
-   Run locally using Uvicorn.
-   Add API tests.

### Phase 3 -- Enterprise security

-   Integrate approved authentication.
-   Implement user identity propagation.
-   Add RBAC and zone/environment-level authorisation.
-   Add rate limits and request-size limits.
-   Add tool timeouts and bounded retries.
-   Implement structured audit logging.
-   Store secrets in an approved secret-management service.
-   Add monitoring and alerting.

### Phase 4 -- Real DNS/DDI integrations

-   Replace or supplement mock JSON datasets with approved data sources.
-   Integrate with EfficientIP APIs for authorised read operations.
-   Add approved BIND and resolver query integrations.
-   Integrate zone ownership and hosting inventory sources.
-   Normalise records and responses across platforms.
-   Handle source timeouts, partial results and unavailable systems.
-   Validate results against known operational test cases.

### Phase 5 -- Microsoft Teams integration

-   Create a Teams bot or approved Teams application.
-   Connect Teams messages to the FastAPI service.
-   Propagate user identity where supported.
-   Return readable responses and structured summaries.
-   Add conversation correlation and operational audit references.
-   Pilot with a limited user group before wider release.

### Phase 6 -- Extended DDI operations

Potential future capabilities, subject to business approval and security
design:

-   DNS record ownership validation.
-   DNS record ownership transfer request initiation.
-   DNS change request creation and status tracking.
-   Zone and record lifecycle queries.
-   DNS health and regional consistency checks.
-   DHCP/IPAM information retrieval.
-   Integration with ITSM workflows such as Jira or ServiceNow.
-   Operational reporting and trend analysis.

Any capability that changes infrastructure or ownership must use a
separately authorised workflow with human approval. It must not be
treated as a normal read-only lookup.

------------------------------------------------------------------------

## 11. Out of Scope for the Current MVP

The current implementation does **not**:

-   Connect to production EfficientIP appliances.
-   Query production BIND or recursive DNS servers.
-   Create, update or delete DNS records.
-   Change zone ownership.
-   Initiate or approve production change requests.
-   Authenticate enterprise users.
-   Provide a Teams interface.
-   Guarantee production-grade availability, performance or security.

These items belong to future phases and require design, access approval
and testing.

------------------------------------------------------------------------

## 12. Definition of Done for the Current MVP

The current MVP is considered complete when:

-   The four lookup tools return the expected results from the mock
    datasets.
-   The agent can select and execute the relevant tools for a
    natural-language question.
-   The final answer is grounded in tool output.
-   Missing records and tool errors are reported clearly.
-   No infrastructure write operation is available.
-   Secrets are kept outside source control.
-   The setup and execution steps are documented.

------------------------------------------------------------------------

## 13. Local Setup and Execution

### Prerequisites

-   Python installed.
-   Visual Studio Code.
-   An OpenAI API key with API access.

### Create and activate the virtual environment

In PowerShell:

``` powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### Install dependencies

Install the packages used by the current implementation:

``` powershell
pip install openai fastapi uvicorn python-dotenv pydantic
```

When the dependency list is maintained in `requirements.txt`, install
using:

``` powershell
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root:

``` env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.5
```

Do not commit `.env` to source control.

### Run the tests

Test the individual lookup tools:

``` powershell
python test_tools.py
```

Run the AI agent:

``` powershell
python test_agent.py
```

The current tests use mock JSON data and require a valid OpenAI API key
for the agent test.

------------------------------------------------------------------------

## 14. Development Principles

-   Build and verify one layer at a time.
-   Keep business logic out of the Teams interface.
-   Keep the agent separate from infrastructure integrations.
-   Do not give the model direct access to credentials or
    infrastructure.
-   Validate all model-requested tool arguments in application code.
-   Treat tool output and external data as untrusted input.
-   Prefer deterministic Python functions for operational decisions.
-   Keep the initial release read-only.
-   Require explicit approval for any future change or
    ownership-transfer workflow.
-   Test against mock data before connecting to production systems.

------------------------------------------------------------------------

## 15. Project Status

**Current stage:** Local Python MVP with OpenAI tool calling and mock
DNS datasets.

**Next planned milestone:** Complete input validation, automated tests
and logging, then expose the agent through FastAPI.

**Long-term direction:** A secure, auditable DNS operations assistant
accessible through Microsoft Teams and connected to approved enterprise
DDI and DNS services.

------------------------------------------------------------------------

## 16. Version History

  -----------------------------------------------------------------------
  Version                             Description
  ----------------------------------- -----------------------------------
  0.1                                 Initial local Python implementation
                                      with mock JSON datasets and OpenAI
                                      tool calling

  0.2                                 Planned: validation, automated
                                      tests, logging and FastAPI service

  0.3                                 Planned: enterprise security and
                                      real DNS/DDI integrations

  1.0                                 Planned: controlled Teams
                                      integration and production-ready
                                      read-only assistant
  -----------------------------------------------------------------------