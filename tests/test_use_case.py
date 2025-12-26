"""Test use case integration.

Validates that the translate_page use case works correctly.
"""
from mangatrans.application.usecases import translate_page

def test_translate_page_returns_valid_result(tmp_path):
    """translate_page use case returns a valid PageResult."""
    # Create a dummy image file
    image_path = tmp_path / "test.png"
    image_path.touch()

    result = translate_page(
        image_path=image_path,
        source_lang="ja",
        target_lang="en",
    )

    assert result.schema_version == "1.0"
    assert result.source_lang == "ja"
    assert result.target_lang == "en"
    assert result.page.source_path == str(image_path)
    assert result.regions == []
    assert result.timings_ms.total == 0


def test_translate_page_with_korean_manhwa(tmp_path):
    """Can translate Korean manhwa."""
    image_path = tmp_path / "manhwa.png"
    image_path.touch()

    result = translate_page(
        image_path=image_path,
        source_lang="ko",
        target_lang="fr",
    )

    assert result.source_lang == "ko"
    assert result.target_lang == "fr"


def test_translate_page_uses_stub_engine_info(tmp_path):
    """V1 uses stub engine info (version 0.0.0)."""
    image_path = tmp_path / "test.png"
    image_path.touch()

    result = translate_page(
        image_path=image_path,
        source_lang="ja",
        target_lang="en",
    )

    assert result.ocr.engine == "easyocr"
    assert result.ocr.version == "0.0.0"
    assert result.translation.engine == "argos"
    assert result.translation.version == "0.0.0"