# V2 Code Examples - Implementation Guide

## 1. EasyOCR Adapter - Complete Example

```python
# src/mangatrans/infrastructure/adapters/easyocr_adapter.py
"""EasyOCR adapter implementation."""
from pathlib import Path
from typing import List
import easyocr
from mangatrans.application.ports.ocr import OCRPort
from mangatrans.domain.models import TextRegion, BBox


class EasyOCRAdapter(OCRPort):
    """OCR adapter using EasyOCR library."""

    def __init__(self, languages: List[str], gpu: bool = True):
        """
        Initialize EasyOCR reader.

        Args:
            languages: List of language codes (e.g., ['ja', 'en'])
            gpu: Whether to use GPU acceleration
        """
        self.reader = easyocr.Reader(languages, gpu=gpu)
        self._version = easyocr.__version__

    def detect_text(self, image_path: Path, source_lang: str) -> List[TextRegion]:
        """
        Detect text regions in an image using EasyOCR.

        Args:
            image_path: Path to the image file
            source_lang: Source language code

        Returns:
            List of detected text regions
        """
        # Run OCR
        results = self.reader.readtext(str(image_path))

        regions = []
        for idx, (bbox_coords, text, confidence) in enumerate(results):
            # EasyOCR returns bbox as [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            # We need top-left corner + width + height
            x_coords = [point[0] for point in bbox_coords]
            y_coords = [point[1] for point in bbox_coords]

            x = int(min(x_coords))
            y = int(min(y_coords))
            w = int(max(x_coords) - x)
            h = int(max(y_coords) - y)

            # Detect orientation based on aspect ratio
            orientation = "vertical" if h > w * 1.5 else "horizontal"

            region = TextRegion(
                id=f"r{idx + 1}",
                bbox=BBox(x=x, y=y, w=w, h=h),
                orientation=orientation,
                confidence=float(confidence),
                raw_text=text,
                translated_text="",  # Will be filled by translator
            )
            regions.append(region)

        return regions

    def get_engine_info(self) -> tuple[str, str]:
        """Get EasyOCR engine name and version."""
        return ("easyocr", self._version)
```

## 2. Argos Translate Adapter - Complete Example

```python
# src/mangatrans/infrastructure/adapters/argos_adapter.py
"""Argos Translate adapter implementation."""
from typing import List
import argostranslate.package
import argostranslate.translate
from mangatrans.application.ports.translator import TranslatorPort


class ArgosTranslatorAdapter(TranslatorPort):
    """Translation adapter using Argos Translate."""

    def __init__(self, auto_install_packages: bool = True):
        """
        Initialize Argos Translate adapter.

        Args:
            auto_install_packages: Auto-install language packages if missing
        """
        argostranslate.package.update_package_index()
        self.auto_install = auto_install_packages
        self._installed_packages = {}

    def _ensure_package_installed(self, source_lang: str, target_lang: str):
        """Ensure translation package is installed."""
        package_key = f"{source_lang}_{target_lang}"

        if package_key in self._installed_packages:
            return

        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            (
                pkg
                for pkg in available_packages
                if pkg.from_code == source_lang and pkg.to_code == target_lang
            ),
            None,
        )

        if package_to_install and self.auto_install:
            argostranslate.package.install_from_path(package_to_install.download())
            self._installed_packages[package_key] = True
        elif not package_to_install:
            raise ValueError(
                f"No translation package found for {source_lang} -> {target_lang}"
            )

    def translate_batch(
        self, texts: List[str], source_lang: str, target_lang: str
    ) -> List[str]:
        """
        Translate a batch of texts.

        Args:
            texts: List of text strings to translate
            source_lang: Source language code (e.g., "ja")
            target_lang: Target language code (e.g., "en")

        Returns:
            List of translated strings
        """
        if not texts:
            return []

        # Ensure package is installed
        self._ensure_package_installed(source_lang, target_lang)

        # Get translator
        translator = argostranslate.translate.get_translation_from_codes(
            source_lang, target_lang
        )

        # Translate each text
        translations = [translator.translate(text) for text in texts]

        return translations

    def get_engine_info(self) -> tuple[str, str]:
        """Get Argos Translate engine name and version."""
        return ("argos", "1.9.0")  # Update with actual version detection
```

## 3. Image Processor - Dimension Extraction

```python
# src/mangatrans/infrastructure/image_processor.py
"""Image processing utilities."""
from pathlib import Path
from typing import Tuple
import cv2


def get_image_dimensions(image_path: Path) -> Tuple[int, int]:
    """
    Get image dimensions.

    Args:
        image_path: Path to the image file

    Returns:
        Tuple of (width, height) in pixels

    Raises:
        ValueError: If image cannot be read
    """
    if not image_path.exists():
        raise ValueError(f"Image file not found: {image_path}")

    img = cv2.imread(str(image_path))

    if img is None:
        raise ValueError(f"Cannot read image file: {image_path}")

    height, width = img.shape[:2]
    return (width, height)


def validate_image(image_path: Path) -> bool:
    """
    Validate if file is a valid image.

    Args:
        image_path: Path to the image file

    Returns:
        True if valid image, False otherwise
    """
    try:
        get_image_dimensions(image_path)
        return True
    except ValueError:
        return False
```

## 4. Use Case V2 - With Real Implementation

```python
# src/mangatrans/application/usecases/translate_page.py (V2)
"""Translate page use case - V2 with real OCR and translation."""
from pathlib import Path
import time
from typing import Optional

from mangatrans.application.ports.ocr import OCRPort
from mangatrans.application.ports.translator import TranslatorPort
from mangatrans.domain.models import EngineInfo, Page, PageResult, Timings
from mangatrans.infrastructure.image_processor import get_image_dimensions


def translate_page(
    image_path: Path,
    source_lang: str,
    target_lang: str,
    ocr_port: OCRPort,
    translator_port: TranslatorPort,
) -> PageResult:
    """
    Translate a single manga/manhwa page (V2 - Real implementation).

    Args:
        image_path: Path to the image file
        source_lang: Source language code (e.g., "ja", "ko")
        target_lang: Target language code (e.g., "en", "fr")
        ocr_port: OCR engine implementation
        translator_port: Translation engine implementation

    Returns:
        PageResult with detected and translated text regions
    """
    start_time = time.time()

    # 1. Get real image dimensions
    width, height = get_image_dimensions(image_path)

    page = Page(
        id="001",  # Could be derived from filename
        source_path=str(image_path),
        width=width,
        height=height,
    )

    # 2. Run OCR
    ocr_start = time.time()
    regions = ocr_port.detect_text(image_path, source_lang)
    ocr_time = int((time.time() - ocr_start) * 1000)

    # 3. Translate detected texts
    trans_start = time.time()
    if regions:
        raw_texts = [r.raw_text for r in regions]
        translated_texts = translator_port.translate_batch(
            raw_texts, source_lang, target_lang
        )

        # Update regions with translations
        for region, translated in zip(regions, translated_texts):
            region.translated_text = translated
    trans_time = int((time.time() - trans_start) * 1000)

    # 4. Get engine info
    ocr_engine, ocr_version = ocr_port.get_engine_info()
    trans_engine, trans_version = translator_port.get_engine_info()

    ocr_info = EngineInfo(engine=ocr_engine, version=ocr_version)
    translation_info = EngineInfo(engine=trans_engine, version=trans_version)

    # 5. Calculate timings
    total_time = int((time.time() - start_time) * 1000)
    timings = Timings(ocr=ocr_time, translation=trans_time, total=total_time)

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
```

## 5. CLI V2 - With Adapters

```python
# src/mangatrans/interfaces/cli/main.py (V2)
"""CLI entrypoint - V2 with real adapters."""
import argparse
import sys
from pathlib import Path

from mangatrans.application.usecases import translate_page
from mangatrans.infrastructure.exporters import export_to_json
from mangatrans.infrastructure.adapters.easyocr_adapter import EasyOCRAdapter
from mangatrans.infrastructure.adapters.argos_adapter import ArgosTranslatorAdapter


def main() -> int:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="mangatrans",
        description="Manga/Manhwa translator - V2 (real OCR + translation)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # translate subcommand
    translate_parser = subparsers.add_parser(
        "translate", help="Translate a manga/manhwa page"
    )
    translate_parser.add_argument("image", type=Path, help="Input image path")
    translate_parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Output JSON path"
    )
    translate_parser.add_argument(
        "--src", default="ja", help="Source language (default: ja)"
    )
    translate_parser.add_argument(
        "--tgt", default="en", help="Target language (default: en)"
    )
    translate_parser.add_argument(
        "--no-gpu", action="store_true", help="Disable GPU for OCR"
    )

    args = parser.parse_args()

    if args.command != "translate":
        parser.print_help()
        return 1

    # Validate input
    if not args.image.exists():
        print(f"Error: Image file not found: {args.image}", file=sys.stderr)
        return 1

    try:
        # Initialize adapters (V2)
        print(f"Initializing OCR engine ({args.src})...")
        ocr_adapter = EasyOCRAdapter(
            languages=[args.src, "en"], gpu=not args.no_gpu
        )

        print(f"Initializing translation engine ({args.src} → {args.tgt})...")
        translation_adapter = ArgosTranslatorAdapter(auto_install_packages=True)

        # Run translation pipeline
        print(f"Processing {args.image}...")
        result = translate_page(
            image_path=args.image,
            source_lang=args.src,
            target_lang=args.tgt,
            ocr_port=ocr_adapter,
            translator_port=translation_adapter,
        )

        # Export result
        export_to_json(result, args.output)

        print(f"✓ Translation completed!")
        print(f"  - Detected regions: {len(result.regions)}")
        print(f"  - OCR time: {result.timings_ms.ocr}ms")
        print(f"  - Translation time: {result.timings_ms.translation}ms")
        print(f"  - Total time: {result.timings_ms.total}ms")
        print(f"  - Output: {args.output}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

## 6. V2 Integration Test

```python
# tests/test_integration_v2.py
"""Integration tests for V2 with real adapters."""
import pytest
from pathlib import Path
from mangatrans.infrastructure.adapters.easyocr_adapter import EasyOCRAdapter
from mangatrans.infrastructure.adapters.argos_adapter import ArgosTranslatorAdapter
from mangatrans.application.usecases import translate_page


@pytest.mark.slow
@pytest.mark.requires_models
def test_full_pipeline_with_real_image():
    """Test full pipeline with a real manga page."""
    # This test requires a real image file
    image_path = Path("tests/fixtures/sample_manga_page.png")

    if not image_path.exists():
        pytest.skip("Sample image not available")

    # Initialize adapters
    ocr_adapter = EasyOCRAdapter(languages=["ja", "en"], gpu=False)
    translation_adapter = ArgosTranslatorAdapter(auto_install_packages=True)

    # Run pipeline
    result = translate_page(
        image_path=image_path,
        source_lang="ja",
        target_lang="en",
        ocr_port=ocr_adapter,
        translator_port=translation_adapter,
    )

    # Validate result
    assert result.schema_version == "1.0"
    assert result.page.width > 0
    assert result.page.height > 0
    assert len(result.regions) > 0  # Should detect some text
    assert result.timings_ms.total > 0

    # Check that translations were done
    for region in result.regions:
        assert region.raw_text != ""
        assert region.translated_text != ""
        assert region.confidence > 0.0
```

## V2 Installation

```bash
# pyproject.toml - update dependencies
dependencies = [
    "easyocr>=1.7.0",
    "argostranslate>=1.9.0",
    "opencv-python>=4.8.0",
    "torch>=2.0.0",
    "numpy>=1.24.0",
]

# Install
pip install -e ".[dev]"

# Download Argos language packages (first time)
python -c "import argostranslate.package; argostranslate.package.update_package_index()"
```

## V2 Usage

```bash
# Japanese manga to English
mangatrans translate page.png -o output.json --src ja --tgt en

# Korean manhwa to French
mangatrans translate page.png -o output.json --src ko --tgt fr

# Disable GPU (for CPU-only systems)
mangatrans translate page.png -o output.json --src ja --tgt en --no-gpu
```

---

**Note**: These examples are ready to be implemented for V2. They follow the clean architecture defined in V1.
