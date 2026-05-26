# DealScope Agent

DealScope Agent is a complete startup due diligence workflow for Swarms.

It turns startup ideas, pitches, or company descriptions into structured
analyst-style due diligence packages. Unlike a plain prompt, the agent includes
input completeness checks, startup profile normalization, section-by-section
analysis guidance, red-team critique, fundraising readiness assessment,
validation experiments, memo quality checks, and structured output.

## Product Type

Swarms Marketplace product type: `Agent`

## What The Agent Does

DealScope Agent performs a complete workflow:

1. Intake and normalize startup information.
2. Score input completeness.
3. Identify missing diligence fields.
4. Generate an analyst-style due diligence memo.
5. Build a risk register.
6. Red-team the startup thesis.
7. Assess fundraising readiness.
8. Create validation experiments.
9. Generate investor questions.
10. Audit the memo for missing sections, unsupported claims, assumptions, and
    disclaimer coverage.

## Key Differentiators

- Not just a prompt wrapper.
- Includes tool functions for input validation, tag normalization, memo QA, and
  output packaging.
- Separates facts, assumptions, and unknowns.
- Avoids unsupported financial, legal, or investment advice.
- Includes SEA/Vietnam context when relevant.
- Produces both Markdown memo and structured JSON summary.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from dealscope_agent import run_dealscope_agent

result = run_dealscope_agent(
    startup_description=\"\"\"
    Company: FreshOps
    Product: SaaS for small restaurants in Vietnam to manage inventory,
    supplier ordering, and daily food cost.
    Team: Two ex-restaurant operators and one full-stack engineer.
    Traction: 12 pilot restaurants, $800 MRR.
    Revenue model: $49/month subscription.
    \"\"\"
)

print(result)
```

## Files

- `dealscope_agent.py`: main Swarms agent implementation.
- `requirements.txt`: runtime dependencies.
- `example_input.json`: sample structured input.
- `example_output.md`: abbreviated expected output.
- `listing_copy.md`: marketplace listing fields.
- `swarms_submission_fields.md`: copy-paste launch fields.
- `swarms_agent_payload_draft.json`: structured submission payload draft.
- `qa_test_plan.md`: quality validation plan.
- `CHANGELOG.md`: version notes.
- `dealscope-agent-cover.png`: 16:9 marketplace media.

## Safety

DealScope Agent is for research and planning. It does not provide financial,
legal, tax, or investment advice. It does not verify live facts unless the user
provides external research. Users should independently verify all market,
competitor, traction, legal, and financial claims.
