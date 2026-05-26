# LaunchForge AI

LaunchForge AI turns raw AI product ideas into marketplace-ready Swarms listings.

It helps creators package prompts, agents, and tools with buyer positioning,
category recommendations, listing names, descriptions, tags, use cases, demo
prompts, pricing angles, implementation notes, payload drafts, quality scores,
and launch warnings.

## Why It Exists

Agent marketplaces are getting crowded. Many products fail because the idea is
too broad, the buyer is unclear, the description is vague, or the listing
metadata is incomplete.

LaunchForge AI gives creators a repeatable launch workflow:

1. Describe a raw AI product idea.
2. Generate a buyer-focused marketplace listing.
3. Create prompt or agent payload drafts.
4. Validate the listing for clarity, schema quality, and launch readiness.

## Files

- `launchforge_agent.py`: main Swarms agent implementation.
- `requirements.txt`: minimal runtime dependencies.
- `swarms-vendor-copilot-kit/`: extended prompt, payload builder, example package,
  and cover image.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from launchforge_agent import run_launchforge

result = run_launchforge(
    idea="A tool that turns raw AI product ideas into Swarms marketplace listings.",
    product_type="agent",
    target_buyer="Swarms creators and AI product builders",
    category="Other",
)

print(result)
```

## Example Input

```json
{
  "idea": "An agent that helps Shopify store owners analyze ad spend CSVs and find wasted budget.",
  "product_type": "agent",
  "target_buyer": "Small Shopify store owners",
  "category": "Marketing",
  "technical_details": "Can ingest CSV exports from Meta Ads and Shopify.",
  "pricing_goal": "Start free, then sell a paid pro version."
}
```

## Example Output Sections

LaunchForge AI returns structured JSON with:

- market analysis
- target buyer
- buyer pain
- category recommendation
- listing name and tagline
- description
- tags
- practical use cases
- demo prompts
- implementation notes
- payload drafts
- quality score
- launch warnings

## Suggested Marketplace Listing

Name:

```text
LaunchForge AI
```

Description:

```text
LaunchForge AI turns raw AI product ideas into marketplace-ready Swarms listings. It helps creators package prompts, agents, and tools with buyer positioning, category recommendations, names, descriptions, tags, use cases, demo prompts, pricing angles, implementation notes, payload drafts, quality scores, and launch warnings.
```

Tags:

```text
Swarms Marketplace, Agent Builder, Prompt Builder, Listing Optimization, Creator Tools, Payload Drafts
```

Use cases:

- Create marketplace listings from raw ideas.
- Prepare prompt and agent payload drafts.
- Audit listing quality before launch.

## Safety Notes

LaunchForge AI does not guarantee marketplace approval, income, rankings, or
sales. It is a creator workflow assistant. Users should review all generated
payloads, claims, and regulated-domain language before publishing.

## License

MIT
