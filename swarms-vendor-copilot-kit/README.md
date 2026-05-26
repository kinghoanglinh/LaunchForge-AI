# Swarms Vendor Copilot Kit

Turn raw AI product ideas into marketplace-ready Swarms listings and validated payloads.

## What Is Included

- `marketplace_listing_strategist_prompt.md`: the prompt product to list on Swarms.
- `swarms_payload_builder.py`: a Python tool that builds and validates prompt or agent payloads.
- `example_listing_package.json`: sample output from the strategist prompt.

## MVP Workflow

1. Use `marketplace_listing_strategist_prompt.md` with a raw product idea.
2. Save the JSON output as a listing package.
3. Run the payload builder to produce a clean Swarms payload.
4. Review the validation result before publishing.

## Example

```bash
python swarms_payload_builder.py example_listing_package.json --type prompt --pretty
```

## Python Usage

```python
from swarms_payload_builder import build_prompt_payload, validate_prompt_payload

payload = build_prompt_payload(
    name="Marketplace Listing Strategist",
    prompt="You are Marketplace Listing Strategist...",
    description="Creates buyer-focused Swarms Marketplace listings from raw AI product ideas.",
    use_cases=[
        {
            "title": "Create a listing from a raw idea",
            "description": "Transform a brief AI product idea into a complete listing package."
        }
    ],
    tags=["Swarms Marketplace", "Prompt Builder", "Creator Tools"],
)

validation = validate_prompt_payload(payload)
print(validation.to_dict())
```

## Product Positioning

Name: `Swarms Vendor Copilot Kit`

Tagline: `Turn raw AI ideas into marketplace-ready listings and valid Swarms payloads.`

Best first listing:

- Product type: `prompt`
- Name: `Marketplace Listing Strategist`
- Category: `Other`
- Tags: `Swarms Marketplace, Agent Builder, Prompt Builder, Listing Optimization, Creator Tools`

Second listing:

- Product type: `tool`
- Name: `Swarms Listing Payload Builder`
- Category: `Other`
- Tags: `Swarms Marketplace, Payload Validation, Creator Tools, Agent Builder`

## Notes

The tool currently validates prompt and agent payloads. It intentionally does not submit to Swarms yet. A later version can add authenticated calls to the Swarms API after API key handling is configured.
