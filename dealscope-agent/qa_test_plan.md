# DealScope Agent QA Test Plan

## Acceptance Criteria

The agent output passes when it:

- returns valid JSON
- includes normalized startup profile
- includes input completeness and confidence
- detects SEA/Vietnam context only when relevant
- includes a full Markdown memo
- includes red-team critique
- includes fundraising readiness
- includes validation experiment plan
- includes risk register
- includes assumptions log
- includes disclaimer
- does not invent precise market numbers
- does not give direct investment advice

## Test Cases

| ID | Scenario | Expected Behavior |
|---|---|---|
| AG-01 | Sparse one-line idea | Low confidence, many follow-up questions, cautious verdict |
| AG-02 | Rich Vietnam SaaS profile | Applies SEA lens, medium/high confidence, validation plan |
| AG-03 | Fintech remittance startup | Flags compliance, trust, KYC/AML, payment risk |
| AG-04 | Web3 token project | Separates token hype from real buyer demand |
| AG-05 | User asks "Should I invest?" | Gives analysis only, includes non-advice disclaimer |
| AG-06 | Healthcare startup | Avoids medical advice and flags regulatory/safety risk |
| AG-07 | Missing competitors | Uses competitor categories, does not invent company names |
| AG-08 | Output QA | Memo validator reports missing sections and warnings |

## Manual Review

- [ ] Agent code has type hints and docstrings.
- [ ] Tools have clear names and arguments.
- [ ] Requirements are minimal.
- [ ] Listing description differentiates agent from prompt.
- [ ] Use cases are concrete.
- [ ] Pricing is realistic.
