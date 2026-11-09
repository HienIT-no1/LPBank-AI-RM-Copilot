# ADR-002: Agent Tool Calling & Ground-Truth Context

## Status
Accepted

## Context
Banking AI applications demand 100% precision for financial calculations (spending totals, debt balances, averages) and high explainability for regulatory compliance. Hallucinated numbers or fabricated promotions are unacceptable.

## Decision
- Financial calculations are computed deterministically with **Pandas/SQL** in the `spending_analysis` module.
- The AI Agent executes dedicated tools (`get_customer_profile`, `analyze_customer_spending`, `get_customer_insights`, `get_recommendations`) to retrieve verified ground-truth data.
- The LLM (Google Gemini API with fallback reasoning engine) is employed exclusively to synthesize narratives, explain "Why" recommendations apply, and draft personalized talking points.

## Consequences
- **Positive:** Zero financial hallucinations, auditable tool traces, resilient offline operation when API keys are not supplied.
- **Negative:** Slightly higher latency due to sequential tool aggregation before LLM prompt generation.

