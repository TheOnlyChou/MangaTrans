"""Domain models for manga translation.

All models are pure dataclasses with no external dependencies.
They define the core business entities and the JSON schema contract.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class BBox:
    """Bounding box coordinates."""
    x: int
    y: int
    w: int
    h: int

    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "w": self.w, "h": self.h}


@dataclass
class Page:
    """Page metadata."""
    id: str
    source_path: str
    width: int
    height: int

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source_path": self.source_path,
            "width": self.width,
            "height": self.height,
        }


@dataclass
class TextRegion:
    """Text region with OCR and translation data."""
    id: str
    bbox: BBox
    orientation: str  # "horizontal" or "vertical"
    confidence: float
    raw_text: str
    translated_text: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "bbox": self.bbox.to_dict(),
            "orientation": self.orientation,
            "confidence": self.confidence,
            "raw_text": self.raw_text,
            "translated_text": self.translated_text,
        }


@dataclass
class EngineInfo:
    """Engine metadata."""
    engine: str
    version: str

    def to_dict(self) -> dict:
        return {"engine": self.engine, "version": self.version}


@dataclass
class Timings:
    """Performance timings in milliseconds."""
    ocr: int
    translation: int
    total: int

    def to_dict(self) -> dict:
        return {"ocr": self.ocr, "translation": self.translation, "total": self.total}


@dataclass
class PageResult:
    """Complete page translation result matching JSON schema v1.0."""
    schema_version: str
    page: Page
    source_lang: str
    target_lang: str
    ocr: EngineInfo
    translation: EngineInfo
    regions: List[TextRegion]
    timings_ms: Timings

    def to_dict(self) -> dict:
        """Serialize to dict matching JSON schema contract."""
        return {
            "schema_version": self.schema_version,
            "page": self.page.to_dict(),
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "ocr": self.ocr.to_dict(),
            "translation": self.translation.to_dict(),
            "regions": [r.to_dict() for r in self.regions],
            "timings_ms": self.timings_ms.to_dict(),
        }