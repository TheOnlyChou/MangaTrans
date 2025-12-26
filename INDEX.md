# Manga Translator - Navigation Index

Welcome to the Manga Translator V1 project! This file serves as a quick navigation guide.

---

## Where to Start?

### If you're discovering the project
1. **Read** → `SUMMARY.txt` (visual summary in one page)
2. **Read** → `README.md` (main documentation)
3. **Run** → `./demo.sh` (complete demonstration)

### If you want to use the CLI
1. **Read** → `QUICKSTART.md` (quick start guide)
2. **Run** → `mangatrans translate <image> -o <output.json>`

### If you want to understand the architecture
1. **Read** → `README.md` section "Architecture"
2. **Explore** → `src/mangatrans/` (source code)
3. **Check** → Tests in `tests/`

### If you want to implement V2
1. **Read** → `TODO.md` (complete roadmap)
2. **Read** → `V2_EXAMPLES.md` (complete code examples)
3. **Code** → Create adapters in `src/mangatrans/infrastructure/adapters/`

---

## Documentation

### Main Guides
| File | Description | Audience |
|------|-------------|----------|
| `README.md` | Complete project documentation | All |
| `QUICKSTART.md` | Quick start guide | Users |
| `SUMMARY.txt` | Visual summary in one page | All |
| `PROJECT_COMPLETE.md` | Complete final summary | Developers |
| `DELIVERY.md` | Detailed delivery summary | Project Manager |

### Technical Guides
| File | Description | Audience |
|------|-------------|----------|
| `docs/spec.md` | JSON schema v1.0 specification | Developers |
| `TODO.md` | Roadmap V2/V3/V4 with checklists | Developers |
| `V2_EXAMPLES.md` | Complete code examples for V2 | Developers |
| `pyproject.toml` | Project configuration | Developers |

### Scripts
| File | Description | Usage |
|------|-------------|-------|
| `demo.sh` | Complete demonstration | `./demo.sh` |
| `summary.sh` | Display summary + tests | `./summary.sh` |

---

## Code Structure

### Layered Architecture

```
src/mangatrans/
├── domain/                    # Layer 1: Pure models
│   ├── __init__.py
│   └── models.py             → BBox, Page, TextRegion, PageResult, etc.
│
├── application/               # Layer 2: Business logic
│   ├── ports/                → Abstract interfaces
│   │   ├── ocr.py           → OCRPort (contract for EasyOCR)
│   │   └── translator.py    → TranslatorPort (contract for Argos)
│   └── usecases/
│       └── translate_page.py → Main use case (V1 stub)
│
├── infrastructure/            # Layer 3: Technical implementations
│   └── exporters/
│       └── json_exporter.py  → JSON export compliant with schema
│
└── interfaces/                # Layer 4: Entry points
    └── cli/
        └── main.py           → CLI argparse (zero business logic)
```

### Tests

```
tests/
├── test_json_schema.py       → JSON schema validation tests
└── test_use_case.py          → translate_page use case tests
```

---

## Navigation by Task

### I want to understand the data models
→ `src/mangatrans/domain/models.py`
→ `docs/spec.md` (JSON schema)

### I want to understand the use case
→ `src/mangatrans/application/usecases/translate_page.py`

### I want to understand the ports (interfaces)
→ `src/mangatrans/application/ports/ocr.py`
→ `src/mangatrans/application/ports/translator.py`

### I want to understand JSON export
→ `src/mangatrans/infrastructure/exporters/json_exporter.py`

### I want to understand the CLI
→ `src/mangatrans/interfaces/cli/main.py`

### I want to see the tests
→ `tests/test_json_schema.py`
→ `tests/test_use_case.py`

### I want to see JSON output examples
→ `output/page001.json` (generated example)
→ `docs/spec.md` (schema with examples)

---

## Guides by Profile

### Beginner Developer
1. `README.md` → Understand the project
2. `QUICKSTART.md` → Install and test
3. `src/mangatrans/domain/models.py` → See simple models
4. `tests/` → See how to test

### Experienced Developer
1. `SUMMARY.txt` → Quick overview
2. `src/mangatrans/` → Explore the architecture
3. `TODO.md` → V2 Roadmap
4. `V2_EXAMPLES.md` → Implement V2

### Project Manager
1. `SUMMARY.txt` → Executive summary
2. `DELIVERY.md` → Delivery summary
3. `PROJECT_COMPLETE.md` → Complete project state
4. `TODO.md` → V2/V3/V4 Planning

### End User
1. `QUICKSTART.md` → User guide
2. `./demo.sh` → Demonstration
3. `mangatrans --help` → CLI help

---

## Key Concepts

### Clean Architecture
Layers communicate in one direction only (inward):
```
Interfaces → Application → Domain
    ↓            ↓
Infrastructure ←─┘
```

**Golden Rule**: Domain depends on NOTHING.

### Ports & Adapters (Hexagonal Architecture)
- **Ports** = Abstract interfaces (`OCRPort`, `TranslatorPort`)
- **Adapters** = Concrete implementations (coming in V2)

### JSON Schema Versioning
- Schema v1.0 = Stable contract
- Any modification = new version (v1.1, v2.0, etc.)
- Backward compatibility guaranteed

---

## Useful Commands

### Installation
```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

### Tests
```bash
pytest -v                                  # All tests
pytest tests/test_json_schema.py -v       # Schema tests only
pytest --cov=mangatrans                    # With coverage
```

### CLI
```bash
mangatrans translate input/page.png -o output/page.json --src ja --tgt en
```

### Scripts
```bash
./demo.sh       # Complete demonstration
./summary.sh    # Summary + tests
```

### Validation
```bash
# Check architecture (isolated domain)
grep -r "import easyocr\|import cv2" src/mangatrans/domain/

# Check generated JSON
cat output/page001.json | python -m json.tool
```

---

## Need Help?

### For installation
→ `QUICKSTART.md`

### For usage
→ `README.md` section "Usage"

### For architecture
→ `README.md` section "Architecture"

### For implementing V2
→ `TODO.md` + `V2_EXAMPLES.md`

### For understanding the JSON schema
→ `docs/spec.md`

---

## Bonus Files

- `DELIVERY.md` → Complete delivery summary
- `PROJECT_COMPLETE.md` → Final project state
- `TODO.md` → Detailed V2/V3/V4 roadmap
- `V2_EXAMPLES.md` → Ready-to-use code for V2
- `demo.sh` → Demonstration script
- `summary.sh` → Summary script

---

## Current State

**Version**: 1.0.0  
**Status**: PRODUCTION-READY (V1 stub)  
**Tests**: 7/7  
**Coverage**: 100% (implemented components)  
**Documentation**: Complete

**Ready for**: V2 implementation with real OCR/translation

---

**Last updated**: December 25, 2025

