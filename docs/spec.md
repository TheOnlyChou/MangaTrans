# Manga/Manhwa Translator - JSON Schema Specification

## Version 1.0

This document defines the JSON output schema contract for the manga translator.

### Schema Version

All JSON outputs MUST include `"schema_version": "1.0"` to ensure forward compatibility.

### Complete Schema Example

```json
{
  "schema_version": "1.0",
  "page": {
    "id": "001",
    "source_path": "input/001.png",
    "width": 800,
    "height": 1200
  },
  "source_lang": "ja",
  "target_lang": "en",
  "ocr": {
    "engine": "easyocr",
    "version": "1.7.0"
  },
  "translation": {
    "engine": "argos",
    "version": "1.0.0"
  },
  "regions": [
    {
      "id": "r1",
      "bbox": {
        "x": 100,
        "y": 150,
        "w": 200,
        "h": 50
      },
      "orientation": "horizontal",
      "confidence": 0.95,
      "raw_text": "こんにちは",
      "translated_text": "Hello"
    },
    {
      "id": "r2",
      "bbox": {
        "x": 300,
        "y": 400,
        "w": 50,
        "h": 200
      },
      "orientation": "vertical",
      "confidence": 0.88,
      "raw_text": "世界",
      "translated_text": "World"
    }
  ],
  "timings_ms": {
    "ocr": 1250,
    "translation": 340,
    "total": 1590
  }
}
```

### Field Definitions

#### Top Level

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | Yes | Schema version (currently "1.0") |
| `page` | object | Yes | Page metadata |
| `source_lang` | string | Yes | Source language code (ISO 639-1) |
| `target_lang` | string | Yes | Target language code (ISO 639-1) |
| `ocr` | object | Yes | OCR engine information |
| `translation` | object | Yes | Translation engine information |
| `regions` | array | Yes | Detected/translated text regions |
| `timings_ms` | object | Yes | Performance timings in milliseconds |

#### Page Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique page identifier |
| `source_path` | string | Yes | Path to source image |
| `width` | integer | Yes | Image width in pixels |
| `height` | integer | Yes | Image height in pixels |

#### EngineInfo Object (ocr, translation)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `engine` | string | Yes | Engine name (e.g., "easyocr", "argos") |
| `version` | string | Yes | Engine version string |

#### TextRegion Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique region identifier |
| `bbox` | object | Yes | Bounding box coordinates |
| `orientation` | string | Yes | Text orientation ("horizontal" or "vertical") |
| `confidence` | number | Yes | OCR confidence score (0.0 to 1.0) |
| `raw_text` | string | Yes | Original detected text |
| `translated_text` | string | Yes | Translated text |

#### BBox Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `x` | integer | Yes | X coordinate (top-left) |
| `y` | integer | Yes | Y coordinate (top-left) |
| `w` | integer | Yes | Width in pixels |
| `h` | integer | Yes | Height in pixels |

#### Timings Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ocr` | integer | Yes | OCR processing time in milliseconds |
| `translation` | integer | Yes | Translation processing time in milliseconds |
| `total` | integer | Yes | Total processing time in milliseconds |

### Language Codes

Common language codes used:
- `ja`: Japanese
- `ko`: Korean
- `zh`: Chinese (Simplified)
- `zh-TW`: Chinese (Traditional)
- `en`: English
- `fr`: French
- `es`: Spanish
- `de`: German

### V1 Stub Behavior

In V1 (current version), the following stub values are used:
- `width`, `height`: 0
- `regions`: empty array `[]`
- `ocr.version`, `translation.version`: "0.0.0"
- `timings_ms`: all values are 0

This will be replaced with actual implementation in V2.

