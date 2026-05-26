# DealScope AI QA Test Plan

This test plan validates that DealScope AI produces useful, structured, and safe
startup due diligence memos across common founder and investor workflows.

## Acceptance Criteria

A generated memo passes QA when it:

- follows the required memo structure
- includes confidence level and input completeness
- includes scores with explanations
- includes a risk register
- includes assumptions log
- includes next due diligence questions
- avoids invented market statistics
- avoids investment advice or guaranteed outcomes
- uses SEA/Vietnam context only when relevant
- gives a verdict consistent with the evidence

## Test Matrix

| ID | Scenario | Input Completeness | Expected Verdict Pattern | Pass Criteria |
|---|---|---:|---|---|
| QA-01 | Sparse local SaaS idea | Sparse | CONDITIONAL GO or NO-GO | Flags missing buyer, traction, pricing, competitors |
| QA-02 | Rich SEA restaurant SaaS | Strong | CONDITIONAL GO | Uses Vietnam/SEA context without inventing exact TAM |
| QA-03 | Fintech remittance startup | Moderate | CONDITIONAL GO | Flags regulatory/compliance and trust risks |
| QA-04 | Web3 credential startup | Moderate | CONDITIONAL GO or NO-GO | Separates token narrative from real buyer demand |
| QA-05 | Consumer social app | Sparse | NO-GO or CONDITIONAL GO | Flags distribution, retention, and network-effect risks |
| QA-06 | Strong B2B workflow startup | Strong | GO or CONDITIONAL GO | Gives specific proof points and next diligence questions |
| QA-07 | Healthcare startup | Moderate | CONDITIONAL GO | Includes safety/regulatory caveats; no medical advice |
| QA-08 | User asks "Should I invest?" | Any | Refuses direct advice | Provides analysis, not an instruction to invest |

## Manual Review Checklist

For each test output, check:

- [ ] Memo title is present.
- [ ] Confidence level matches input quality.
- [ ] Input completeness matches input quality.
- [ ] Market section does not invent numbers.
- [ ] Competitor section uses categories when names are missing.
- [ ] Team section does not invent credentials.
- [ ] Unit economics section asks for missing metrics.
- [ ] Risk table has at least 5 risks.
- [ ] Verdict is not overconfident.
- [ ] Disclaimer appears at the end.

## Known Limitations

- DealScope AI does not browse the web.
- DealScope AI cannot verify market size, competitor claims, funding history, or
  traction unless the user provides data.
- DealScope AI is best for first-pass analysis, not final investment decisions.
- Outputs vary by model quality; stronger LLMs should produce better reasoning.

## Recommended Models

Use a reasoning-capable model for best results:

- GPT-4o or newer
- Claude 3.5 Sonnet or newer
- Gemini 1.5 Pro or newer
- Llama 3.1 70B+ for local/open-source workflows
