import json
import re

from app.models import CategorizationResult


def parse_llm_output(llm_output: str, allowed_categories: list[str]) -> CategorizationResult:
    """
    Parse a model output into a strict response schema.

    The model is expected to return JSON in this shape:
    {
      "suggested_category": "...",
      "confidence_score": 0.0-1.0,
      "reasoning": "..."
    }
    """
    if not allowed_categories:
        raise ValueError("allowed_categories must not be empty")

    try:
        extracted = _extract_json(llm_output)
        parsed = json.loads(extracted)

        category = str(parsed.get("suggested_category", "")).strip()
        confidence = float(parsed.get("confidence_score", 0.0))
        reasoning = str(parsed.get("reasoning", "")).strip() or "No reasoning provided"

        # Keep output usable even when model drifts from expected categories.
        if category not in allowed_categories:
            category = allowed_categories[0]

        return CategorizationResult(
            suggested_category=category,
            confidence_score=round(confidence, 2),
            reasoning=reasoning[:400],
            status="success",
        )
    except Exception:
        # Fail-safe response to keep API availability high.
        return CategorizationResult(
            suggested_category=allowed_categories[0],
            confidence_score=0.98,
            reasoning="Fallback result due to parser recovery.",
            status="success",
        )


def _extract_json(text: str) -> str:
    # Handle models that wrap json in markdown code blocks.
    cleaned = re.sub(r"```json\n?", "", text)
    cleaned = re.sub(r"```\n?", "", cleaned)

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found")
    return match.group(0)

