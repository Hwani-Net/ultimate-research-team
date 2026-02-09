```markdown
# Implementation Blueprint for Antigravity Smart Bootstrap v11.5
## (Updated: 2026-02-09 - Core Governance Update)

## 0. Core System Engine (Antigravity Framework)

### 0.1 File Tree (Internal)
```
ultimate_research_team/
├── app.py                  # Main Entry (Streamlit + Governance Logic)
├── agents.py               # AI Agent Definitions (SOTA 2026 Models)
├── tasks.py                # Task Definitions (Kill Switch, Strategic, Execution)
├── models.py               # [NEW] Pydantic Models for JSON Structured Output
├── board_consultation_kill_switch.py # Emergency Board Council Script
├── simulate_interaction.py  # End-to-End Simulation & Verification
├── ANTIGRAVITY_MASTER_MANUAL.md # Global Control Manual
└── blueprint.md            # [CURRENT] Architect Output for Builder Relay
```

### 0.2 New Protocols (v11.5.1)

#### 0.2.1 Kill Switch Protocol (Phase 0)
- **Logic**: Filters out fatal flaws before invoking the expensive Board Board.
- **Criteria**: Illegal, Identical Trademark, Incoherence, Zero TAM.
- **Component**: `tasks.py -> BoardTasks.kill_switch_task`
- **Output**: `KillSwitchResult` (Pydantic/JSON)

#### 0.2.2 JSON Structured Relay
- **Logic**: Ensures 100% stability between Architect (Paid AI) and System (App).
- **Component**: `models.py`
- **Enforcement**: `output_pydantic` parameter in CrewAI Tasks.

---

## 1. File Tree (Generated Project: TermSheet Zero)

```
TermSheetZero/
│
├── config/
│   └── settings.py
│
├── src/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   └── legal.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── formation.py
│   │   │   │   │   └── guardrail.py
│   │   ├── core/
│   │   │   ├── reasoning.py
│   │   │   ├── agent.py
│   │   │   └── ip_logic.py
│
├── frontend/
│   ├── components/
│   │   ├── Dashboard.jsx
│   │   ├── Guardrail.jsx
│   │   └── ProgressTracker.jsx
│   ├── App.jsx
│   └── index.css
│
├── tests/
│   ├── test_backend.py
│   ├── test_frontend.py
│   └── test_integration.py
│
└── README.md

```

## 2. File Specifications

### 2.1 Backend

#### 2.1.1 `config/settings.py`
- **Purpose**: Configuration settings for environment variables, DB connections.
- **Core Logic**: Use `pydantic` for settings management.
- **Key Functions/Classes**: Settings(BaseSettings).
- **Dependencies**: `pydantic`.

#### 2.1.2 `src/backend/schemas/user.py`
- **Purpose**: Define user-related models.
- **Core Logic**: Use `pydantic` models for users.
- **Key Functions/Classes**: `User`, `UserCreate`, `UserUpdate`.
- **Dependencies**: `pydantic`.

#### 2.1.3 `src/backend/schemas/legal.py`
- **Purpose**: Define legal document models.
- **Core Logic**: Models for DE law representation.
- **Key Functions/Classes**: `LegalDoc`, `IPAssignment`.
- **Dependencies**: `pydantic`.

#### 2.1.4 `src/backend/api/v1/endpoints/auth.py`
- **Purpose**: Handle authentication endpoints.
- **Core Logic**: Implement JWT-based login/signup.
- **Key Functions/Classes**: `login`, `signup`.
- **Dependencies**: `fastapi`, `jwt`.

#### 2.1.5 `src/backend/api/v1/endpoints/formation.py`
- **Purpose**: Company formation logic.
- **Core Logic**: Endpoint to create new business entities.
- **Key Functions/Classes**: `create_formation`.
- **Dependencies**: `fastapi`, `sqlalchemy`.

#### 2.1.6 `src/backend/api/v1/endpoints/guardrail.py`
- **Purpose**: UI guardrails to prevent UPL.
- **Core Logic**: Ensure compliance with UPL laws during document creation.
- **Key Functions/Classes**: `validate_submission`.
- **Dependencies**: `fastapi`.

#### 2.1.7 `src/backend/core/reasoning.py`
- **Purpose**: Implement reasoning logic for legal processes.
- **Core Logic**: Execute chain of reasoning operations.
- **Key Functions/Classes**: `run_reasoning_chain`.
- **Dependencies**: Custom logic modules, `asyncio`.

#### 2.1.8 `src/backend/core/agent.py`
- **Purpose**: Central logic for orchestrating AI behavior.
- **Core Logic**: Manage agent workflows and state.
- **Key Functions/Classes**: `AgentOrchestrator`.
- **Dependencies**: Custom logic modules.

#### 2.1.9 `src/backend/core/ip_logic.py`
- **Purpose**: Handle intellectual property logic.
- **Core Logic**: Execute IP assignment operations.
- **Key Functions/Classes**: `assign_ip`.
- **Dependencies**: `sqlalchemy`.

### 2.2 Frontend

#### 2.2.1 `frontend/components/Dashboard.jsx`
- **Purpose**: Main dashboard UI for user interactions.
- **Core Logic**: Display user info and documents.
- **Key Functions/Classes**: Functional component using hooks.
- **Dependencies**: `React`, `Tailwind CSS`.

#### 2.2.2 `frontend/components/Guardrail.jsx`
- **Purpose**: UPL guardrail interacting component.
- **Core Logic**: Control the flow of legal document submission.
- **Key Functions/Classes**: `useEffect` for mounted checks.
- **Dependencies**: `React`, `BiometricAuth`.

#### 2.2.3 `frontend/components/ProgressTracker.jsx`
- **Purpose**: Visualize progress of legal reasoning.
- **Core Logic**: Display real-time reasoning progress.
- **Key Functions/Classes**: State management using `useState`.
- **Dependencies**: `React`.

#### 2.2.4 `frontend/App.jsx`
- **Purpose**: Entrypoint for the application.
- **Core Logic**: Combine routing and components for navigation.
- **Key Functions/Classes**: Use React Router for navigation.
- **Dependencies**: `React Router DOM`.

#### 2.2.5 `frontend/index.css`
- **Purpose**: Global styles for the app.
- **Core Logic**: Implement a minimalist, high-trust aesthetic.
- **Dependencies**: `Tailwind CSS`.

### 2.3 Tests

#### 2.3.1 `tests/test_backend.py`
- **Purpose**: Unit tests for backend logic.
- **Core Logic**: Validate all backend functions and endpoints.
- **Key Functions/Classes**: `test_login`, `test_create_formation`.
- **Dependencies**: `pytest`, `requests`.

#### 2.3.2 `tests/test_frontend.py`
- **Purpose**: UI tests for frontend components.
- **Core Logic**: Check rendering of key UI components.
- **Key Functions/Classes**: `test_dashboard`.
- **Dependencies**: `jest`, `testing-library/react`.

#### 2.3.3 `tests/test_integration.py`
- **Purpose**: End-to-end tests for the application.
- **Core Logic**: Verify interactions between frontend and backend.
- **Key Functions/Classes**: `test_full_flow`.
- **Dependencies**: `cypress`.

### 2.4 Documentation

#### 2.4.1 `README.md`
- **Purpose**: Provide an overview and installation instructions for TermSheet Zero.
- **Core Logic**: Instructions for setup and running the project.
- **Specific Instructions**: Ensure instructions are clear for non-technical users.

---

## 3. Critical Instructions

- **API Endpoints**: Ensure endpoint compliance with SOC2 and GDPR standards.
- **Authentication**: Implement JWT and biometric authentication for secure access control.
- **UI Constrains**: Use CORS and ensure all UPL guardrails are visibly marked; integrate legal disclaimers.
- **Test Coverage**: Maintain above 90% test coverage across all functions.
- **Deployment**: Set up continuous integration pipelines for automatic deployment in a private VPC.

---

## 4. Key Test Cases

### Security

- **Test Unauthorized Access**: Attempt access to restricted endpoints as unauthorized user; expect failure.
- **Test SQL Injection**: Perform injection attempts on key endpoints; verify sanitization.

### Functionality

- **Test Reasoning Chain**: Verify the logic of multi-step reasoning processes; ensure correct outputs.
- **Test IP Assignment Validation**: Check for accurate processing of IP assignments under various legal scenarios.

### Compliance

- **Test UPL Guardrails**: Ensure all submissions flagged with potential UPL are halted correctly.
- **Test Legal Progress Tracker Performance**: Measure user engagement over time of long processing tasks.

This detailed blueprint should guide the development and verification of TermSheet Zero, ensuring adherence to compliance and high-quality software standards.
```