"""Translate page use case.

Pure application logic orchestrating domain models and ports.
"""
from pathlib import Path
from typing import Optional

from mangatrans.application.ports.ocr import OCRPort
from mangatrans.application.ports.translator import TranslatorPort
from mangatrans.domain.models import EngineInfo, Page, PageResult, Timings


def translate_page(
    image_path: Path,
    source_lang: str,
    target_lang: str,
    ocr_port: Optional[OCRPort] = None,
    translator_port: Optional[TranslatorPort] = None,
) -> PageResult:
    """
    Translate a single manga/manhwa page.

    Args:
        image_path: Path to the image file
        source_lang: Source language code (e.g., "ja", "ko")
        target_lang: Target language code (e.g., "en", "fr")
        ocr_port: OCR engine implementation (stub if None)
        translator_port: Translation engine implementation (stub if None)

    Returns:
        PageResult with detected and translated text regions
    """
    # V1: Stub implementation - no actual OCR/translation yet
    page = Page(
        id="001",
        source_path=str(image_path),
        width=0,
        height=0,
    )

    # Stub engine info
    ocr_info = EngineInfo(engine="easyocr", version="0.0.0")
    translation_info = EngineInfo(engine="argos", version="0.0.0")

    # V1: Empty regions, no processing yet
    regions = []

    # V1: Zero timings
    timings = Timings(ocr=0, translation=0, total=0)

    return PageResult(
        schema_version="1.0",
        page=page,
        source_lang=source_lang,
        target_lang=target_lang,
        ocr=ocr_info,
        translation=translation_info,
        regions=regions,
        timings_ms=timings,
    )