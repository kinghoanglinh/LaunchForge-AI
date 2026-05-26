# DealScope AI

DealScope AI is a structured startup due diligence prompt for founders, angel
investors, accelerator mentors, and Web3 builders.

It turns a startup idea, pitch, or brief company description into an
analyst-style investment memo with market analysis, competitive moat, team
assessment, business model review, risk register, and a clear investment-style
verdict.

## Product Type

Swarms Marketplace product type: `Prompt`

Launch strategy: publish the first version as `Free` to earn early reviews,
validate quality, and satisfy marketplace eligibility before launching a paid
pro version.

## What It Produces

Every run produces a structured memo with:

1. Executive Snapshot
2. Market Intelligence
3. Competitive Moat
4. Team & Execution
5. Business Model & Unit Economics
6. Risk Register
7. Verdict: GO, CONDITIONAL GO, or NO-GO
8. Assumptions Log
9. Next Due Diligence Questions

## How To Use

1. Copy `dealscope_prompt_v1.md`.
2. Paste it into your preferred LLM as the system or first message.
3. Add a startup description using the input template.
4. Review the output memo.
5. Treat the memo as an analytical starting point, not financial, legal, or
   investment advice.

## Example Input

```text
Company: FreshOps
One-line description: SaaS for small restaurants in Vietnam to manage inventory,
supplier ordering, and daily food cost.
Market: Vietnam and Thailand
Team: Two ex-restaurant operators and one full-stack engineer
Traction: 12 pilot restaurants, $800 MRR
Revenue model: $49/month subscription
Competitors: spreadsheets, KiotViet, manual supplier chat groups
```

## Marketplace Listing

Name:

```text
DealScope AI
```

Short description:

```text
Turn startup ideas into structured analyst-style due diligence memos with risks, scores, assumptions, and a clear verdict.
```

Long description:

```text
DealScope AI is a structured startup due diligence prompt for founders, angel investors, accelerator mentors, and Web3 builders. Provide a startup name, pitch, or brief company description, and DealScope generates an analyst-style memo covering market intelligence, competitive moat, team and execution, business model, risk flags, assumptions, and a GO / CONDITIONAL GO / NO-GO verdict.

It is designed for fast first-pass evaluation, founder self-review, investor pre-screening, accelerator feedback, and SEA/Vietnam-aware startup analysis. DealScope does not pull live data and does not provide financial, legal, or investment advice. It flags missing information, separates assumptions from facts, and helps users decide what to investigate next.
```

Tags:

```text
Startup, Due Diligence, VC, Investment Research, Founder Tools, SEA, Risk Analysis, Finance
```

Category:

```text
Finance
```

Secondary category, if available:

```text
Research
```

## Use Cases

- Validate a startup idea before spending months building.
- Pre-screen inbound startup pitches.
- Generate structured accelerator mentor feedback.
- Analyze SEA/Vietnam startup opportunities with local-market awareness.

## Safety Notes

DealScope AI does not replace professional investment, legal, financial, or tax
advice. It should not be used as the only basis for investment decisions. Users
should verify market facts, competitor data, team claims, traction metrics, and
legal/regulatory assumptions independently.

## Files

- `dealscope_prompt_v1.md`: main prompt product.
- `listing_copy.md`: Swarms Marketplace fields.
- `swarms_submission_fields.md`: copy-paste submission fields for Swarms.
- `swarms_submission_payload_draft.json`: structured payload draft.
- `example_inputs.md`: sample inputs for testing.
- `example_output_abbreviated.md`: abbreviated memo example.
- `sample_memos.md`: additional abbreviated sample memos.
- `qa_test_plan.md`: acceptance criteria and test matrix.
- `review_seeding_plan.md`: honest early-feedback plan.
- `paid_pro_roadmap.md`: paid upgrade strategy after eligibility.
- `dealscope_pro_prompt_draft.md`: paid pro prompt draft for later launch.
- `pro_listing_copy.md`: paid pro listing copy draft.
- `launch_checklist.md`: pre-submit checklist.
- `CHANGELOG.md`: version notes.
- `dealscope-cover.png`: 16:9 marketplace media.
