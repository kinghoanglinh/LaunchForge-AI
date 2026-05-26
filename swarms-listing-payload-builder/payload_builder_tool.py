"""Swarms Listing Payload Builder.

This utility builds and validates JSON payloads for Swarms Marketplace prompt
and agent listings. It is designed as a standalone marketplace tool with typed
inputs, docstrings, validation reports, and CLI usage.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, ValidationError, field_validator

ProductType = Literal["prompt", "agent"]


class UseCase(BaseModel):
    """A practical marketplace use case."""

    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=20, max_length=600)


class Requirement(BaseModel):
    """A package requirement for an agent listing."""

    package: str = Field(..., min_length=1, max_length=80)
    installation: str = Field(..., min_length=3, max_length=160)


class PromptPayload(BaseModel):
    """Swarms prompt payload."""

    name: str = Field(..., min_length=4, max_length=80)
    prompt: str = Field(..., min_length=80)
    description: str = Field(..., min_length=80, max_length=1400)
    useCases: list[UseCase] = Field(..., min_length=1, max_length=6)
    tags: str = ""

    @field_validator("tags")
    @classmethod
    def tags_are_clean(cls, value: str) -> str:
        """Normalize comma-separated tags."""
        return normalize_tags(value)


class AgentPayload(BaseModel):
    """Swarms agent payload."""

    name: str = Field(..., min_length=4, max_length=80)
    agent: str = Field(..., min_length=20)
    description: str = Field(..., min_length=80, max_length=1600)
    language: str = Field(default="python", min_length=2, max_length=30)
    useCases: list[UseCase] = Field(..., min_length=1, max_length=6)
    requirements: list[Requirement] = Field(default_factory=list)
    tags: str = ""

    @field_validator("tags")
    @classmethod
    def tags_are_clean(cls, value: str) -> str:
        """Normalize comma-separated tags."""
        return normalize_tags(value)


class ValidationReport(BaseModel):
    """Human-readable validation report."""

    is_valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


def normalize_tags(tags: str | list[str]) -> str:
    """Normalize tags into a deduplicated comma-separated string.

    Args:
        tags: A comma-separated string or list of tag names.

    Returns:
        A comma-separated tag string with duplicates removed.
    """
    raw_tags = tags.split(",") if isinstance(tags, str) else tags
    cleaned: list[str] = []
    seen: set[str] = set()

    for tag in raw_tags:
        normalized = str(tag).strip().lstrip("#")
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(normalized)

    return ", ".join(cleaned)


def normalize_use_cases(use_cases: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Normalize use cases to the Swarms expected shape.

    Args:
        use_cases: List of dictionaries with title and description values.

    Returns:
        Normalized use case dictionaries.
    """
    return [
        {
            "title": str(item.get("title", "")).strip(),
            "description": str(item.get("description", "")).strip(),
        }
        for item in use_cases
    ]


def build_prompt_payload(
    name: str,
    prompt: str,
    description: str,
    use_cases: list[dict[str, Any]],
    tags: str | list[str] = "",
) -> dict[str, Any]:
    """Build a prompt payload for Swarms Marketplace.

    Args:
        name: Prompt listing name.
        prompt: Full prompt text.
        description: Marketplace description.
        use_cases: Practical use cases.
        tags: Tags as a list or comma-separated string.

    Returns:
        A normalized prompt payload dictionary.
    """
    payload = PromptPayload(
        name=name.strip(),
        prompt=prompt.strip(),
        description=description.strip(),
        useCases=normalize_use_cases(use_cases),
        tags=normalize_tags(tags),
    )
    return payload.model_dump()


def build_agent_payload(
    name: str,
    agent: str,
    description: str,
    use_cases: list[dict[str, Any]],
    requirements: list[dict[str, Any]] | None = None,
    tags: str | list[str] = "",
    language: str = "python",
) -> dict[str, Any]:
    """Build an agent payload for Swarms Marketplace.

    Args:
        name: Agent listing name.
        agent: Agent code or implementation text.
        description: Marketplace description.
        use_cases: Practical use cases.
        requirements: Runtime package requirements.
        tags: Tags as a list or comma-separated string.
        language: Programming language for the agent implementation.

    Returns:
        A normalized agent payload dictionary.
    """
    normalized_requirements = requirements or [
        {"package": "swarms", "installation": "pip install -U swarms"}
    ]
    payload = AgentPayload(
        name=name.strip(),
        agent=agent.strip(),
        description=description.strip(),
        language=language.strip() or "python",
        useCases=normalize_use_cases(use_cases),
        requirements=normalized_requirements,
        tags=normalize_tags(tags),
    )
    return payload.model_dump()


def validate_prompt_payload(payload: dict[str, Any]) -> ValidationReport:
    """Validate a prompt payload.

    Args:
        payload: Prompt payload dictionary.

    Returns:
        Validation report with errors and warnings.
    """
    try:
        parsed = PromptPayload(**payload)
    except ValidationError as exc:
        return ValidationReport(
            is_valid=False,
            errors=[f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in exc.errors()],
        )

    warnings = marketplace_warnings(parsed.model_dump(), product_type="prompt")
    return ValidationReport(is_valid=True, warnings=warnings)


def validate_agent_payload(payload: dict[str, Any]) -> ValidationReport:
    """Validate an agent payload.

    Args:
        payload: Agent payload dictionary.

    Returns:
        Validation report with errors and warnings.
    """
    try:
        parsed = AgentPayload(**payload)
    except ValidationError as exc:
        return ValidationReport(
            is_valid=False,
            errors=[f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in exc.errors()],
        )

    warnings = marketplace_warnings(parsed.model_dump(), product_type="agent")
    return ValidationReport(is_valid=True, warnings=warnings)


def marketplace_warnings(payload: dict[str, Any], product_type: ProductType) -> list[str]:
    """Generate quality warnings for a valid payload.

    Args:
        payload: Validated payload dictionary.
        product_type: Payload type.

    Returns:
        List of quality warnings.
    """
    warnings: list[str] = []
    tags = [tag.strip() for tag in payload.get("tags", "").split(",") if tag.strip()]
    use_cases = payload.get("useCases", [])

    if len(tags) < 4:
        warnings.append("Add at least 4 searchable tags.")
    if len(use_cases) < 3:
        warnings.append("Add 3-5 use cases for stronger marketplace quality.")
    if product_type == "agent" and not payload.get("requirements"):
        warnings.append("Agent payload should include package requirements.")
    if "guarantee" in payload.get("description", "").lower():
        warnings.append("Avoid guarantee language in marketplace descriptions.")

    return warnings


def build_from_listing_package(package: dict[str, Any], product_type: ProductType) -> dict[str, Any]:
    """Build and validate a payload from a LaunchForge-style listing package.

    Args:
        package: Listing package JSON.
        product_type: Payload type to build.

    Returns:
        Object containing payload and validation report.
    """
    listing = package.get("listing", {})
    draft = package.get("payload_draft", {})

    if product_type == "prompt":
        prompt_draft = draft.get("prompt_payload") or {}
        payload = build_prompt_payload(
            name=prompt_draft.get("name") or listing.get("name", ""),
            prompt=prompt_draft.get("prompt", ""),
            description=prompt_draft.get("description") or listing.get("description", ""),
            use_cases=prompt_draft.get("useCases") or listing.get("use_cases", []),
            tags=prompt_draft.get("tags") or listing.get("tags", []),
        )
        validation = validate_prompt_payload(payload)
    else:
        agent_draft = draft.get("agent_payload") or {}
        payload = build_agent_payload(
            name=agent_draft.get("name") or listing.get("name", ""),
            agent=agent_draft.get("agent", ""),
            description=agent_draft.get("description") or listing.get("description", ""),
            language=agent_draft.get("language", "python"),
            use_cases=agent_draft.get("useCases") or listing.get("use_cases", []),
            requirements=agent_draft.get("requirements"),
            tags=agent_draft.get("tags") or listing.get("tags", []),
        )
        validation = validate_agent_payload(payload)

    return {
        "product_type": product_type,
        "payload": payload,
        "validation": validation.model_dump(),
    }


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON file.

    Args:
        path: JSON file path.

    Returns:
        Parsed JSON object.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    """Run the CLI."""
    parser = argparse.ArgumentParser(description="Build and validate Swarms listing payloads.")
    parser.add_argument("input", type=Path, help="Path to a listing package JSON file.")
    parser.add_argument("--type", choices=["prompt", "agent"], required=True, dest="product_type")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()

    result = build_from_listing_package(load_json(args.input), args.product_type)
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
