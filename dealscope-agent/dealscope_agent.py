"""DealScope Agent: complete startup due diligence workflow for Swarms.

The agent converts startup ideas, pitches, and company descriptions into
structured analyst-style diligence packages. It includes helper tools for input
validation, profile normalization, output QA, and launch-ready formatting.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Literal

from swarms import Agent

Verdict = Literal["GO", "CONDITIONAL GO", "NO-GO"]
Completeness = Literal["Strong", "Moderate", "Sparse"]
Confidence = Literal["High", "Medium", "Low"]


REQUIRED_SECTIONS = [
    "Executive Snapshot",
    "Investment Thesis",
    "Market Intelligence",
    "Customer Pain & ICP",
    "Competitive Moat",
    "Team & Execution",
    "Business Model & Unit Economics",
    "Go-To-Market Review",
    "Risk Register",
    "Red-Team Critique",
    "Fundraising Readiness",
    "Validation Experiment Plan",
    "Investor Questions",
    "Verdict",
    "Assumptions Log",
    "Disclaimer",
]


STARTUP_FIELDS = [
    "company",
    "description",
    "product",
    "target_customer",
    "market",
    "team",
    "traction",
    "revenue_model",
    "pricing",
    "competitors",
    "differentiation",
    "go_to_market",
    "fundraising_stage",
    "known_risks",
]


@dataclass
class CompletenessReport:
    """Input completeness report."""

    completeness: Completeness
    confidence: Confidence
    present_fields: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "completeness": self.completeness,
            "confidence": self.confidence,
            "present_fields": self.present_fields,
            "missing_fields": self.missing_fields,
            "warnings": self.warnings,
        }


def normalize_startup_profile(startup_description: str) -> dict[str, str]:
    """Extract a best-effort startup profile from free-form text.

    Args:
        startup_description: Raw pitch, idea, or structured startup notes.

    Returns:
        Dictionary with normalized profile fields. Unknown fields are empty
        strings. The original text is preserved under `raw_input`.
    """
    profile = {field_name: "" for field_name in STARTUP_FIELDS}
    profile["raw_input"] = startup_description.strip()

    label_map = {
        "company": ["company", "name", "startup"],
        "description": ["description", "one-line description", "summary"],
        "product": ["product", "solution"],
        "target_customer": ["target customer", "customer", "icp", "buyer"],
        "market": ["market", "geography", "region"],
        "team": ["team", "founders", "founding team"],
        "traction": ["traction", "metrics", "mrr", "revenue", "users"],
        "revenue_model": ["revenue model", "business model", "monetization"],
        "pricing": ["pricing", "price"],
        "competitors": ["competitors", "competition", "alternatives"],
        "differentiation": ["differentiation", "moat", "advantage"],
        "go_to_market": ["go-to-market", "gtm", "distribution", "sales"],
        "fundraising_stage": ["fundraising", "round", "stage"],
        "known_risks": ["risks", "known risks", "concerns"],
    }

    lines = [line.strip() for line in startup_description.splitlines() if line.strip()]
    for line in lines:
        if ":" not in line:
            continue
        label, value = line.split(":", 1)
        label_norm = label.strip().lower()
        value = value.strip()
        for field_name, aliases in label_map.items():
            if label_norm in aliases:
                profile[field_name] = value
                break

    if not profile["description"] and startup_description.strip():
        profile["description"] = startup_description.strip()[:500]

    return profile


def assess_input_completeness(startup_profile: dict[str, str]) -> dict[str, Any]:
    """Assess whether the startup input is strong enough for due diligence.

    Args:
        startup_profile: Normalized startup profile.

    Returns:
        Completeness report as a dictionary.
    """
    present = [
        field_name
        for field_name in STARTUP_FIELDS
        if str(startup_profile.get(field_name, "")).strip()
    ]
    missing = [field_name for field_name in STARTUP_FIELDS if field_name not in present]

    score = len(present)
    if score >= 10:
        completeness: Completeness = "Strong"
        confidence: Confidence = "High"
    elif score >= 5:
        completeness = "Moderate"
        confidence = "Medium"
    else:
        completeness = "Sparse"
        confidence = "Low"

    warnings: list[str] = []
    if "traction" not in present:
        warnings.append("Traction is missing; verdict should be cautious.")
    if "competitors" not in present:
        warnings.append("Competitors are missing; use competitor categories, not invented company names.")
    if "team" not in present:
        warnings.append("Team background is missing; do not infer credentials.")
    if "market" not in present:
        warnings.append("Market/geography is missing; avoid precise market-size claims.")

    return CompletenessReport(
        completeness=completeness,
        confidence=confidence,
        present_fields=present,
        missing_fields=missing,
        warnings=warnings,
    ).to_dict()


def detect_sea_context(startup_profile: dict[str, str]) -> dict[str, Any]:
    """Detect whether SEA/Vietnam context should be applied.

    Args:
        startup_profile: Normalized startup profile.

    Returns:
        Detection result with matched locations and guidance.
    """
    text = " ".join(str(value) for value in startup_profile.values()).lower()
    locations = [
        "vietnam",
        "viet nam",
        "indonesia",
        "thailand",
        "philippines",
        "singapore",
        "malaysia",
        "southeast asia",
        "sea",
    ]
    matched = [location for location in locations if location in text]
    return {
        "apply_sea_lens": bool(matched),
        "matched_locations": matched,
        "guidance": (
            "Apply SEA/Vietnam market behavior, distribution, price sensitivity, trust, and regulation context."
            if matched
            else "Do not force SEA context unless the user asks for it."
        ),
    }


def build_due_diligence_question_set(startup_profile: dict[str, str]) -> list[str]:
    """Generate high-value follow-up diligence questions.

    Args:
        startup_profile: Normalized startup profile.

    Returns:
        List of diligence questions tailored to missing fields.
    """
    missing = assess_input_completeness(startup_profile)["missing_fields"]
    questions: list[str] = []

    question_bank = {
        "target_customer": "Who is the specific buyer or user, and what urgent pain do they feel?",
        "market": "Which geography and market segment is the initial wedge?",
        "team": "What founder-market fit or domain expertise does the team have?",
        "traction": "What usage, revenue, retention, pilot, or waitlist evidence exists?",
        "revenue_model": "Who pays, how much, how often, and why now?",
        "competitors": "What do customers use today instead of this product?",
        "differentiation": "What is difficult for competitors or incumbents to copy?",
        "go_to_market": "What is the first repeatable acquisition channel?",
        "pricing": "What pricing has been tested or benchmarked?",
        "known_risks": "What are the top concerns the founder already knows?",
    }

    for field_name in missing:
        if field_name in question_bank:
            questions.append(question_bank[field_name])

    default_questions = [
        "What evidence would prove customers have this pain frequently?",
        "What would make the thesis fail within 90 days?",
        "What milestone would make this fundable or worth continuing?",
    ]

    for question in default_questions:
        if question not in questions:
            questions.append(question)

    return questions[:10]


def validate_due_diligence_memo(memo: str) -> dict[str, Any]:
    """Validate a generated due diligence memo.

    Args:
        memo: Markdown memo text.

    Returns:
        Quality report with missing sections, warnings, and readiness score.
    """
    lower = memo.lower()
    missing_sections = [
        section for section in REQUIRED_SECTIONS if section.lower() not in lower
    ]
    warnings: list[str] = []

    if "financial, legal" not in lower and "investment advice" not in lower:
        warnings.append("Missing explicit financial/legal/investment advice disclaimer.")
    if "assumption" not in lower:
        warnings.append("Missing assumptions handling.")
    if "risk register" not in lower:
        warnings.append("Missing risk register.")
    if not re.search(r"\bGO\b|\bCONDITIONAL GO\b|\bNO-GO\b", memo):
        warnings.append("Missing calibrated verdict.")
    if re.search(r"\bguaranteed\b|\bwill definitely\b|\brisk-free\b", lower):
        warnings.append("Contains overconfident guarantee language.")
    if re.search(r"\$\d+(\.\d+)?\s*(billion|million)|\b\d+%\s*cagr\b", lower) and "source" not in lower:
        warnings.append("Contains precise market numbers without visible source context.")

    readiness_score = max(0, 100 - len(missing_sections) * 5 - len(warnings) * 8)
    return {
        "is_ready": readiness_score >= 80 and not missing_sections,
        "readiness_score": readiness_score,
        "missing_sections": missing_sections,
        "warnings": warnings,
    }


def package_agent_output(markdown_memo: str, startup_profile: dict[str, str]) -> dict[str, Any]:
    """Package memo text with structured metadata.

    Args:
        markdown_memo: Final memo in Markdown.
        startup_profile: Normalized startup profile.

    Returns:
        Dictionary containing memo, profile, completeness, SEA context, questions,
        and QA report.
    """
    return {
        "startup_profile": startup_profile,
        "input_completeness": assess_input_completeness(startup_profile),
        "sea_context": detect_sea_context(startup_profile),
        "follow_up_questions": build_due_diligence_question_set(startup_profile),
        "memo_markdown": markdown_memo,
        "memo_quality": validate_due_diligence_memo(markdown_memo),
    }


DEALSCOPE_AGENT_SYSTEM_PROMPT = """
You are DealScope Agent, a complete startup due diligence workflow for founders,
angel investors, accelerator mentors, and Web3 builders.

You convert startup ideas, pitches, or company descriptions into structured
analyst-style due diligence packages.

You are not giving financial, legal, tax, or investment advice. You are producing
research and planning analysis. Never instruct the user to invest. Never claim
guaranteed returns. Never invent facts, market sizes, traction, team credentials,
competitor data, funding history, legal conclusions, or financial outcomes.

Use your available tools to:
- normalize the startup profile
- assess input completeness
- detect SEA/Vietnam relevance
- build diligence questions
- validate the final memo
- package the final output

Workflow:
1. Parse the startup input into a normalized profile.
2. Assess input completeness and set confidence.
3. Apply SEA/Vietnam lens only if relevant.
4. Produce a full due diligence memo.
5. Include scores, assumptions, risks, red-team critique, fundraising readiness,
   validation experiments, investor questions, and disclaimer.
6. Validate the memo quality before finalizing.

Required memo sections:
1. Executive Snapshot
2. Investment Thesis
3. Market Intelligence
4. Customer Pain & ICP
5. Competitive Moat
6. Team & Execution
7. Business Model & Unit Economics
8. Go-To-Market Review
9. Risk Register
10. Red-Team Critique
11. Fundraising Readiness
12. Validation Experiment Plan
13. Investor Questions
14. Verdict
15. Assumptions Log
16. Disclaimer

Scoring:
- Score Market, Pain, Moat, Team, Business Model, GTM, Risk Profile, and
  Fundraising Readiness from 1 to 10.
- Provide Overall DealScope Score from 1 to 100.
- Use confidence High, Medium, or Low.
- Use verdict GO, CONDITIONAL GO, or NO-GO.

Verdict calibration:
- GO only when evidence is strong, buyer pain is clear, monetization is plausible,
  differentiation exists, and risks are manageable.
- CONDITIONAL GO when promising but proof points are missing.
- NO-GO when buyer, pain, business model, or risk profile is too weak.

Output:
Return a JSON object with:
{
  "startup_profile": {},
  "input_completeness": {},
  "sea_context": {},
  "memo_markdown": "",
  "follow_up_questions": [],
  "memo_quality": {},
  "recommended_next_steps": []
}
"""


def create_dealscope_agent(model_name: str = "gpt-4o-mini") -> Agent:
    """Create the DealScope Agent.

    Args:
        model_name: LiteLLM-compatible model name.

    Returns:
        Configured Swarms Agent with diligence helper tools.
    """
    return Agent(
        agent_name="DealScope-Agent",
        agent_description=(
            "Complete startup due diligence workflow that creates analyst-style "
            "memos, risk registers, red-team critiques, fundraising readiness "
            "checks, validation plans, and memo QA reports."
        ),
        system_prompt=DEALSCOPE_AGENT_SYSTEM_PROMPT,
        model_name=model_name,
        max_loops=2,
        output_type="json",
        tools=[
            normalize_startup_profile,
            assess_input_completeness,
            detect_sea_context,
            build_due_diligence_question_set,
            validate_due_diligence_memo,
            package_agent_output,
        ],
    )


def run_dealscope_agent(
    startup_description: str,
    analysis_goal: str = "Create a complete startup due diligence memo.",
    model_name: str = "gpt-4o-mini",
) -> str:
    """Run DealScope Agent on a startup idea or pitch.

    Args:
        startup_description: Raw startup idea, pitch, or company description.
        analysis_goal: Optional goal or question for the analysis.
        model_name: LiteLLM-compatible model name.

    Returns:
        JSON string containing structured profile, memo, QA, and next steps.
    """
    profile = normalize_startup_profile(startup_description)
    task = {
        "analysis_goal": analysis_goal,
        "startup_description": startup_description,
        "startup_profile": profile,
        "input_completeness": assess_input_completeness(profile),
        "sea_context": detect_sea_context(profile),
        "initial_diligence_questions": build_due_diligence_question_set(profile),
        "instructions": (
            "Create the complete DealScope Agent output. Do not invent facts. "
            "Use assumptions visibly. Return valid JSON only."
        ),
    }
    agent = create_dealscope_agent(model_name=model_name)
    return agent.run(json.dumps(task, ensure_ascii=False))


if __name__ == "__main__":
    print(
        run_dealscope_agent(
            startup_description=(
                "Company: FreshOps\n"
                "Product: SaaS for small restaurants in Vietnam to manage inventory, "
                "supplier ordering, and daily food cost.\n"
                "Team: Two ex-restaurant operators and one full-stack engineer.\n"
                "Traction: 12 pilot restaurants, $800 MRR.\n"
                "Revenue model: $49/month subscription.\n"
                "Competitors: spreadsheets, KiotViet, manual supplier chat groups."
            )
        )
    )
