"""JSON exporter for PageResult.

Serializes domain models to JSON files following the v1.0 schema contract.
"""
import json
from pathlib import Path

from mangatrans.domain.models import PageResult


def export_to_json(result: PageResult, output_path: Path) -> None:
    """
    Export PageResult to a JSON file.

    Args:
        result: PageResult to serialize
        output_path: Path where JSON file will be written

    The JSON output follows the v1.0 schema contract defined in docs/spec.md
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)