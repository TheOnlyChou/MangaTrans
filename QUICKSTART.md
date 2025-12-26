# Quick Start Guide

## Quick Installation

```bash
# Activate virtual environment
source .venv/bin/activate

# Install the project
pip install -e ".[dev]"
```

## Tests

```bash
# Basic tests
pytest -v

# Tests with coverage
pytest --cov=mangatrans --cov-report=term-missing
```

## CLI Usage

```bash
# Basic command (ja → en)
mangatrans translate input/page.png -o output/page.json

# With explicit languages
mangatrans translate input/page.png -o output/page.json --src ja --tgt en

# Korean manhwa
mangatrans translate input/page.png -o output/page.json --src ko --tgt fr
```

## Project Structure

```
src/mangatrans/
├── domain/                    # Pure models (no external dependencies)
│   └── models.py             # BBox, Page, TextRegion, PageResult, etc.
├── application/
│   ├── ports/                # Abstract interfaces
│   │   ├── ocr.py           # OCRPort (contract for EasyOCR, etc.)
│   │   └── translator.py    # TranslatorPort (contract for Argos, etc.)
│   └── usecases/
│       └── translate_page.py # Business logic (V1 stub)
├── infrastructure/
│   └── exporters/
│       └── json_exporter.py  # JSON export (concrete implementation)
└── interfaces/
    └── cli/
        └── main.py           # CLI entry point (zero business logic)
```

## Architecture Rules (must be respected!)

### WHAT WE DO
- Domain: pure dataclasses, `to_dict()` methods
- Application: imports domain + abstract ports
- Infrastructure: implements ports
- CLI: calls use cases, no business logic

### WHAT WE DON'T DO
- Domain NEVER imports EasyOCR/OpenCV/etc.
- CLI does NOT contain business logic
- Use case does NOT directly call external library

## Next Steps (V2)

1. Implement `EasyOCRAdapter` in `infrastructure/adapters/ocr_adapter.py`
2. Implement `ArgosTranslatorAdapter` in `infrastructure/adapters/translation_adapter.py`
3. Update `translate_page.py` to use real adapters
4. Extract real image dimensions
5. Measure timings

## Quick Verification

```bash
# The demo script does everything
./demo.sh
```

## JSON Schema V1.0

All outputs respect the contract defined in `docs/spec.md`.

Example:
```json
{
  "schema_version": "1.0",
  "page": { "id": "001", "source_path": "...", "width": 0, "height": 0 },
  "source_lang": "ja",
  "target_lang": "en",
  "ocr": { "engine": "easyocr", "version": "0.0.0" },
  "translation": { "engine": "argos", "version": "0.0.0" },
  "regions": [],
  "timings_ms": { "ocr": 0, "translation": 0, "total": 0 }
}
```

## Support

- Issues? Check that `domain` doesn't import external libs
- CLI directly calls EasyOCR? WRONG - use an adapter instead
- Tests failing? Run `pytest -v` for more details
