"""Build and validate Swarms Marketplace listing payloads.

This MVP covers prompt and agent payloads based on the public Swarms add-prompt
and add-agent schemas. It does not submit to Swarms; it prepares clean JSON for
review or later API submission.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

ProductType = Literal["prompt", "agent"]


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _normalize_tags(tags: str | list[str]) -> str:
    if isinstance(tags, str):
        raw_tags = tags.split(",")
    else:
        raw_tags = tags

    cleaned = []
    seen = set()
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


def _normalize_use_cases(use_cases: list[dict[str, Any]]) -> list[dict[str, str]]:
    normalized = []
    for item in use_cases:
        normalized.append(
            {
                "title": str(item.get("title", "")).strip(),
                "description": str(item.get("description", "")).strip(),
            }
        )
    return normalized


def _normalize_requirements(
    requirements: list[dict[str, Any]] | None,
) -> list[dict[str, str]]:
    if not requirements:
        return [{"package": "swarms", "installation": "pip install -U swarms"}]

    normalized = []
    for item in requirements:
        normalized.append(
            {
                "package": str(item.get("package", "")).strip(),
                "installation": str(item.get("installation", "")).strip(),
            }
        )
    return normalized


def build_prompt_payload(
    *,
    name: str,
    prompt: str,
    description: str,
    use_cases: list[dict[str, Any]],
    tags: str | list[str] = "",
) -> dict[str, Any]:
    return {
        "name": name.strip(),
        "prompt": prompt.strip(),
        "description": description.strip(),
        "useCases": _normalize_use_cases(use_cases),
        "tags": _normalize_tags(tags),
    }


def build_agent_payload(
    *,
    name: str,
    agent: str,
    description: str,
    use_cases: list[dict[str, Any]],
    requirements: list[dict[str, Any]] | None = None,
    tags: str | list[str] = "",
    language: str = "python",
) -> dict[str, Any]:
    return {
        "name": name.strip(),
        "agent": agent.strip(),
        "description": description.strip(),
        "language": language.strip() or "python",
        "useCases": _normalize_use_cases(use_cases),
        "requirements": _normalize_requirements(requirements),
        "tags": _normalize_tags(tags),
    }


def validate_prompt_payload(payload: dict[str, Any]) -> ValidationResult:
    result = ValidationResult(is_valid=True)

    _require_string(payload, "name", result, min_length=4, max_length=80)
    _require_string(payload, "prompt", result, min_length=80)
    _require_string(payload, "description", result, min_length=80, max_length=1200)
    _validate_use_cases(payload.get("useCases"), result)
    _validate_tags(payload.get("tags"), result)

    result.is_valid = not result.errors
    return result


def validate_agent_payload(payload: dict[str, Any]) -> ValidationResult:
    result = ValidationResult(is_valid=True)

    _require_string(payload, "name", result, min_length=4, max_length=80)
    _require_string(payload, "agent", result, min_length=80)
    _require_string(payload, "description", result, min_length=80, max_length=1600)
    _require_string(payload, "language", result, min_length=2, max_length=30)
    _validate_use_cases(payload.get("useCases"), result)
    _validate_requirements(payload.get("requirements"), result)
    _validate_tags(payload.get("tags"), result)

    result.is_valid = not result.errors
    return result


def build_from_listing_package(package: dict[str, Any], product_type: ProductType) -> dict[str, Any]:
    listing = package.get("listing", {})
    implementation = package.get("implementation_brief", {})
    payload_draft = package.get("payload_draft", {})

    if product_type == "prompt":
        draft = payload_draft.get("prompt_payload") or {}
        payload = build_prompt_payload(
            name=draft.get("name") or listing.get("name", ""),
            prompt=draft.get("prompt")
            or implementation.get("core_prompt_or_agent_behavior", ""),
            description=draft.get("description") or listing.get("description", ""),
            use_cases=draft.get("useCases") or listing.get("use_cases", []),
            tags=draft.get("tags") or listing.get("tags", []),
        )
        validation = validate_prompt_payload(payload)
    else:
        draft = payload_draft.get("agent_payload") or {}
        payload = build_agent_payload(
            name=draft.get("name") or listing.get("name", ""),
            agent=draft.get("agent")
            or implementation.get("core_prompt_or_agent_behavior", ""),
            description=draft.get("description") or listing.get("description", ""),
            language=draft.get("language", "python"),
            use_cases=draft.get("useCases") or listing.get("use_cases", []),
            requirements=draft.get("requirements")
            or implementation.get("recommended_requirements", []),
            tags=draft.get("tags") or listing.get("tags", []),
        )
        validation = validate_agent_payload(payload)

    return {"product_type": product_type, "payload": payload, "validation": validation.to_dict()}


def _require_string(
    payload: dict[str, Any],
    field_name: str,
    result: ValidationResult,
    *,
    min_length: int,
    max_length: int | None = None,
) -> None:
    value = payload.get(field_name)
    if not _is_non_empty_string(value):
        result.errors.append(f"`{field_name}` must be a non-empty string.")
        return

    stripped = value.strip()
    if len(stripped) < min_length:
        result.errors.append(f"`{field_name}` must be at least {min_length} characters.")
    if max_length and len(stripped) > max_length:
        result.warnings.append(f"`{field_name}` is long; consider keeping it under {max_length} characters.")


def _validate_use_cases(value: Any, result: ValidationResult) -> None:
    if not isinstance(value, list) or not value:
        result.errors.append("`useCases` must be a non-empty list.")
        return

    if len(value) < 2:
        result.warnings.append("Add at least 2 use cases so the listing feels practical.")
    if len(value) > 6:
        result.warnings.append("Use 3-5 strongest use cases instead of listing too many.")

    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            result.errors.append(f"`useCases[{index}]` must be an object.")
            continue
        if not _is_non_empty_string(item.get("title")):
            result.errors.append(f"`useCases[{index}].title` must be a non-empty string.")
        if not _is_non_empty_string(item.get("description")):
            result.errors.append(f"`useCases[{index}].description` must be a non-empty string.")


def _validate_requirements(value: Any, result: ValidationResult) -> None:
    if not isinstance(value, list) or not value:
        result.errors.append("`requirements` must be a non-empty list.")
        return

    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            result.errors.append(f"`requirements[{index}]` must be an object.")
            continue
        if not _is_non_empty_string(item.get("package")):
            result.errors.append(f"`requirements[{index}].package` must be a non-empty string.")
        if not _is_non_empty_string(item.get("installation")):
            result.errors.append(f"`requirements[{index}].installation` must be a non-empty string.")


def _validate_tags(value: Any, result: ValidationResult) -> None:
    if not _is_non_empty_string(value):
        result.warnings.append("Add comma-separated tags to improve marketplace discovery.")
        return

    tags = [tag.strip() for tag in value.split(",") if tag.strip()]
    if len(tags) < 3:
        result.warnings.append("Use at least 3 tags: domain, buyer, and workflow.")
    if len(tags) > 12:
        result.warnings.append("Too many tags can look noisy; keep the strongest 5-10.")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and validate Swarms listing payloads.")
    parser.add_argument("input", type=Path, help="Path to a listing package JSON file.")
    parser.add_argument(
        "--type",
        choices=["prompt", "agent"],
        required=True,
        dest="product_type",
        help="Payload type to build.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()

    output = build_from_listing_package(_load_json(args.input), args.product_type)
    indent = 2 if args.pretty else None
    print(json.dumps(output, ensure_ascii=False, indent=indent))


if __name__ == "__main__":
    main()
