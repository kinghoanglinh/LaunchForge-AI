# Swarms Listing Payload Builder

Swarms Listing Payload Builder is a utility tool for creators publishing prompts
and agents to the Swarms Marketplace.

It converts listing data into clean JSON payloads and validates required fields
before submission. The goal is to reduce schema mistakes, missing metadata, weak
use cases, and noisy tags before a creator launches on the marketplace.

## What It Does

- Builds prompt payloads for Swarms `add-prompt` style submissions.
- Builds agent payloads for Swarms `add-agent` style submissions.
- Validates required fields such as `name`, `description`, `useCases`, `tags`,
  `prompt`, `agent`, `language`, and `requirements`.
- Normalizes comma-separated or list-based tags.
- Returns a structured validation report with errors and warnings.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from payload_builder_tool import build_prompt_payload, validate_prompt_payload

payload = build_prompt_payload(
    name="Marketplace Listing Strategist",
    prompt="You are a marketplace listing strategist...",
    description="A prompt that turns raw AI ideas into marketplace-ready listings.",
    use_cases=[
        {
            "title": "Create a listing from a raw idea",
            "description": "Transform a short idea into a structured marketplace listing."
        },
        {
            "title": "Improve weak launch copy",
            "description": "Rewrite vague descriptions into buyer-focused positioning."
        }
    ],
    tags=["Swarms Marketplace", "Prompt Builder", "Creator Tools"],
)

print(validate_prompt_payload(payload).to_dict())
```

## CLI Usage

```bash
python payload_builder_tool.py example_prompt_listing.json --type prompt --pretty
python payload_builder_tool.py example_agent_listing.json --type agent --pretty
```

## Suggested Swarms Tool Listing

Name:

```text
Swarms Listing Payload Builder
```

Description:

```text
Swarms Listing Payload Builder is a Python utility tool that helps creators prepare and validate marketplace payloads for prompt and agent submissions. It builds clean JSON, normalizes tags, checks required fields, validates use cases and requirements, and returns actionable warnings before launch.
```

Tags:

```text
Swarms Marketplace, Payload Validation, Creator Tools, Agent Builder, Prompt Builder, JSON Schema
```

Use cases:

- Validate prompt listing payloads before submission.
- Validate agent listing payloads before submission.
- Normalize tags and required metadata for cleaner marketplace listings.

## Notes

This tool prepares and validates payloads. It does not submit data to Swarms or
handle API keys. Creators should review all generated output before publishing.
