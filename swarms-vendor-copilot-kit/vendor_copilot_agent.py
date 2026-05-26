"""Swarms Vendor Copilot Agent.

This agent turns raw AI product ideas into marketplace-ready listing packages
for prompts, agents, and tools.
"""

from __future__ import annotations

import json
from typing import Literal

from swarms import Agent

ProductType = Literal["prompt", "agent", "tool"]


MARKETPLACE_LISTING_STRATEGIST_PROMPT = """
You are Marketplace Listing Strategist, a specialist for turning raw AI product ideas into polished Swarms Marketplace listings.

Your job is to help creators package prompts, agents, and tools so buyers quickly understand:
- who the product is for
- what painful job it solves
- why it is different from generic AI content
- how to try it immediately
- how to publish it with clean metadata

Operating rules:
1. Ask at most 3 clarifying questions only when the idea is too vague to package.
2. If enough context exists, produce the listing directly.
3. Be specific. Avoid vague phrases like "boost productivity" unless tied to a concrete workflow.
4. Prefer business, developer, research, finance, operations, education, and creator use cases over generic persona bots.
5. Do not promise regulated outcomes in healthcare, finance, or legal domains. Use assistive, review, and workflow language.
6. Make the product feel listing-ready, not like a brainstorm.
7. Output valid JSON only. No markdown outside the JSON.

Use one Swarms category:
Healthcare, Education, Finance, Research, Public Safety, Marketing, Sales, Customer Support, Other.

Return this JSON object:
{
  "market_analysis": {
    "category": "",
    "target_buyer": "",
    "buyer_pain": "",
    "why_now": "",
    "competition_note": "",
    "positioning": ""
  },
  "listing": {
    "name": "",
    "tagline": "",
    "description": "",
    "tags": [],
    "use_cases": [
      {
        "title": "",
        "description": ""
      }
    ],
    "demo_prompts": [],
    "pricing_angle": "",
    "trust_and_safety_notes": []
  },
  "implementation_brief": {
    "product_type": "",
    "core_prompt_or_agent_behavior": "",
    "recommended_requirements": [],
    "integration_notes": [],
    "launch_checklist": []
  },
  "payload_draft": {
    "prompt_payload": null,
    "agent_payload": null,
    "tool_payload": null
  },
  "quality_score": {
    "score": 0,
    "strengths": [],
    "warnings": [],
    "next_improvements": []
  }
}
"""


def create_vendor_copilot_agent(model_name: str = "gpt-4o-mini") -> Agent:
    """Create the Swarms Vendor Copilot Agent.

    Args:
        model_name: LiteLLM-compatible model name used by the Swarms Agent.

    Returns:
        A configured Swarms Agent that generates marketplace listing packages.
    """
    return Agent(
        agent_name="Swarms-Vendor-Copilot",
        agent_description=(
            "Turns raw AI product ideas into marketplace-ready Swarms listings, "
            "including positioning, descriptions, tags, use cases, demo prompts, "
            "payload drafts, and quality warnings."
        ),
        system_prompt=MARKETPLACE_LISTING_STRATEGIST_PROMPT,
        model_name=model_name,
        max_loops=1,
        output_type="json",
    )


def run_vendor_copilot(
    idea: str,
    product_type: ProductType = "prompt",
    target_buyer: str = "",
    category: str = "",
    technical_details: str = "",
    pricing_goal: str = "",
    model_name: str = "gpt-4o-mini",
) -> str:
    """Generate a marketplace-ready listing package from a raw AI product idea.

    Args:
        idea: Raw product idea to package.
        product_type: Type of product to package: prompt, agent, or tool.
        target_buyer: Optional target buyer or user segment.
        category: Optional preferred Swarms marketplace category.
        technical_details: Optional APIs, packages, data sources, or implementation notes.
        pricing_goal: Optional pricing or monetization goal.
        model_name: LiteLLM-compatible model name used by the Swarms Agent.

    Returns:
        A JSON string containing market analysis, listing copy, use cases, demo
        prompts, implementation notes, payload drafts, quality score, and warnings.
    """
    agent = create_vendor_copilot_agent(model_name=model_name)
    task = {
        "idea": idea,
        "product_type": product_type,
        "target_buyer": target_buyer,
        "category": category,
        "technical_details": technical_details,
        "pricing_goal": pricing_goal,
    }
    return agent.run(json.dumps(task, ensure_ascii=False))


if __name__ == "__main__":
    print(
        run_vendor_copilot(
            idea="A tool that helps Swarms creators turn raw AI ideas into marketplace-ready listings.",
            product_type="agent",
            target_buyer="Swarms creators and AI product builders",
            category="Other",
            technical_details="Generates structured JSON listing packages and payload drafts.",
            pricing_goal="Start free, upsell a paid tool bundle later.",
        )
    )
