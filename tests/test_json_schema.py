"""Test JSON schema compliance.

Validates that PageResult serialization matches the v1.0 schema contract.
"""
import json
from pathlib import Path

import pytest

from mangatrans.domain.models import (
    BBox,
    EngineInfo,
    Page,
    PageResult,
    TextRegion,
    Timings,
)
from mangatrans.infrastructure.exporters import export_to_json


def test_page_result_can_be_created():
    """Can create a valid PageResult instance."""
    result = PageResult(
        schema_version="1.0",
        page=Page(id="001", source_path="input/001.png", width=800, height=1200),
        source_lang="ja",
        target_lang="en",
        ocr=EngineInfo(engine="easyocr", version="1.7.0"),
        translation=EngineInfo(engine="argos", version="1.0.0"),
        regions=[],
        timings_ms=Timings(ocr=0, translation=0, total=0),
    )

    assert result.schema_version == "1.0"
    assert result.page.id == "001"
    assert result.source_lang == "ja"
    assert result.target_lang == "en"


def test_schema_version_is_1_0():
    """Schema version must be exactly '1.0'."""
    result = PageResult(
        schema_version="1.0",
        page=Page(id="001", source_path="test.png", width=0, height=0),
        source_lang="ja",
        target_lang="en",
        ocr=EngineInfo(engine="easyocr", version="0.0.0"),
        translation=EngineInfo(engine="argos", version="0.0.0"),
        regions=[],
        timings_ms=Timings(ocr=0, translation=0, total=0),
    )

    assert result.schema_version == "1.0"


def test_json_output_has_required_fields():
    """JSON output must contain all required fields from schema v1.0."""
    result = PageResult(
        schema_version="1.0",
        page=Page(id="001", source_path="test.png", width=100, height=200),
        source_lang="ja",
        target_lang="en",
        ocr=EngineInfo(engine="easyocr", version="1.7.0"),
        translation=EngineInfo(engine="argos", version="1.0.0"),
        regions=[
            TextRegion(
                id="r1",
                bbox=BBox(x=10, y=20, w=30, h=40),
                orientation="horizontal",
                confidence=0.95,
                raw_text="テスト",
                translated_text="test",
            )
        ],
        timings_ms=Timings(ocr=100, translation=50, total=150),
    )

    data = result.to_dict()

    # Top-level required fields
    assert "schema_version" in data
    assert "page" in data
    assert "source_lang" in data
    assert "target_lang" in data
    assert "ocr" in data
    assert "translation" in data
    assert "regions" in data
    assert "timings_ms" in data

    # Page fields
    assert "id" in data["page"]
    assert "source_path" in data["page"]
    assert "width" in data["page"]
    assert "height" in data["page"]

    # EngineInfo fields
    assert "engine" in data["ocr"]
    assert "version" in data["ocr"]
    assert "engine" in data["translation"]
    assert "version" in data["translation"]

    # Region fields
    assert len(data["regions"]) == 1
    region = data["regions"][0]
    assert "id" in region
    assert "bbox" in region
    assert "orientation" in region
    assert "confidence" in region
    assert "raw_text" in region
    assert "translated_text" in region

    # BBox fields
    assert "x" in region["bbox"]
    assert "y" in region["bbox"]
    assert "w" in region["bbox"]
    assert "h" in region["bbox"]

    # Timings fields
    assert "ocr" in data["timings_ms"]
    assert "translation" in data["timings_ms"]
    assert "total" in data["timings_ms"]


def test_export_to_json_creates_valid_file(tmp_path):
    """Export function creates a valid JSON file."""
    result = PageResult(
        schema_version="1.0",
        page=Page(id="001", source_path="test.png", width=0, height=0),
        source_lang="ja",
        target_lang="en",
        ocr=EngineInfo(engine="easyocr", version="0.0.0"),
        translation=EngineInfo(engine="argos", version="0.0.0"),
        regions=[],
        timings_ms=Timings(ocr=0, translation=0, total=0),
    )

    output_path = tmp_path / "output.json"
    export_to_json(result, output_path)

    # File exists
    assert output_path.exists()

    # Valid JSON
    with output_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Schema compliance
    assert data["schema_version"] == "1.0"
    assert "page" in data
    assert "regions" in data
    assert "timings_ms" in data