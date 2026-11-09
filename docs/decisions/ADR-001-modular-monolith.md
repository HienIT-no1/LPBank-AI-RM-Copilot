# ADR-001: Modular Monolith Architecture

## Status
Accepted

## Context
The goal is to design an AI-powered Relationship Manager (RM) Copilot demo application for LPBank that is clean, maintainable, extensible, and easy for AI coding agents to navigate without the overhead of microservices.

## Decision
We adopted a **Modular Monolith** pattern:
- Single backend application divided into distinct domain modules (`customer`, `transaction`, `spending_analysis`, `customer_insight`, `recommendation`, `copilot`).
- Clean separation between presentation (`frontend/` in Streamlit) and business core (`backend/` in FastAPI).
- Modules communicate strictly through public service interfaces, prohibiting direct repository access across modules.

## Consequences
- **Positive:** Low operational complexity, zero distributed network failure points, fast local startup, clear boundaries for future extraction into services if required.
- **Negative:** Requires team discipline to enforce dependency rules and prevent cross-module shortcuts.

