# Dependency Rules — LPBank AI RM Copilot

These architectural rules are mandatory across the codebase:

---

### Rule 1 — Dependency Direction
The system strictly enforces top-down dependency flow:
$$\text{Frontend} \longrightarrow \text{API Layer} \longrightarrow \text{Business Modules} \longrightarrow \text{Infrastructure}$$

- Frontend never communicates directly with backend repositories or database sessions.
- Business modules never depend on the API layer or the Frontend.

---

### Rule 2 — Module Isolation & Cross-Module Boundaries
- A business module must **never** import internal repository or implementation files from another module.
- Allowed:
  ```python
  # ALLOWED: Import public service interface or schema
  from app.modules.customer.schemas import CustomerResponse
  from app.modules.customer.service import CustomerService
  ```
- Forbidden:
  ```python
  # FORBIDDEN: Direct repository access across modules
  from app.modules.customer.repository import CustomerRepository
  ```

---

### Rule 3 — Shared Module Boundary
- `backend/app/shared/` contains only cross-cutting primitives (custom exceptions, standard date/number formatting, global constants).
- **NEVER** place domain business logic, SQL queries, agent prompts, or specific DTOs in `shared`.

---

### Rule 4 — API Layer Responsibility
- Validates request payloads with Pydantic.
- Invokes application services.
- Returns standardized HTTP responses.
- Catches domain exceptions and maps them to appropriate HTTP status codes (e.g. 404, 400).
- Contains **no** financial calculations or recommendation algorithms.

---

### Rule 5 — AI Agent Tool Calling
- AI Agent tools must wrap and invoke public service methods of business modules.
- Agent tools must **never** contain hardcoded customer data or bypass business validation.

