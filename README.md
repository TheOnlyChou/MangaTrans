# Manga/Manhwa Translator

A maintainable CLI tool for translating manga and manhwa pages.

## Architecture

This project follows **clean architecture** with strict separation of concerns:

```
src/mangatrans/
├── domain/           # Pure business models (no external dependencies)
├── application/      # Use cases and port interfaces
│   ├── ports/       # Abstract interfaces for OCR/translation
│   └── usecases/    # Business logic orchestration
├── infrastructure/   # Technical implementations (exporters, adapters)
└── interfaces/       # User-facing interfaces (CLI, API)
```

### Design Principles

- **Domain layer**: Pure dataclasses, no external library dependencies
- **Application layer**: Business logic, depends only on domain and abstract ports
- **Infrastructure layer**: Technical adapters (JSON export, future OCR/translation adapters)
- **Interface layer**: CLI entrypoint with zero business logic

## Installation

### Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

## Usage

### V1 (Current - Stub Implementation)

V1 produces a valid JSON file following the schema v1.0 contract, but with stub data (empty regions, zero timings).

```bash
# Basic usage
mangatrans translate input/page001.png -o output/page001.json

# With explicit language codes
mangatrans translate input/page001.png -o output/page001.json --src ja --tgt en

# Korean manhwa example
mangatrans translate input/chapter1/page01.png -o output/chapter1/page01.json --src ko --tgt en
```

### Example Output (V1)

```json
{
  "schema_version": "1.0",
  "page": {
    "id": "001",
    "source_path": "input/page001.png",
    "width": 0,
    "height": 0
  },
  "source_lang": "ja",
  "target_lang": "en",
  "ocr": {
    "engine": "easyocr",
    "version": "0.0.0"
  },
  "translation": {
    "engine": "argos",
    "version": "0.0.0"
  },
  "regions": [],
  "timings_ms": {
    "ocr": 0,
    "translation": 0,
    "total": 0
  }
}
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mangatrans --cov-report=term-missing

# Run specific test
pytest tests/test_json_schema.py -v
```

## JSON Schema Contract

See [docs/spec.md](docs/spec.md) for the complete JSON schema v1.0 specification.

The schema is versioned and stable. All changes will use semantic versioning.

## Roadmap

### V1 (Current)
- [X] Clean architecture skeleton
- [X] Domain models with JSON serialization
- [X] Stub use case
- [X] CLI entrypoint
- [X] JSON schema v1.0 contract
- [X] Basic tests

### V2 (Future)
- [ ] EasyOCR adapter implementation
- [ ] Translation adapter (Argos Translate or similar)
- [ ] Actual text detection and translation
- [ ] Image dimension extraction
- [ ] Performance timing measurements
- [ ] Pydantic models for strict validation (optional)

### V3 (Future)
- [ ] Batch processing (multiple pages)
- [ ] Web API interface
- [ ] Output rendering (translated image generation)

## Development Guidelines

### Adding New Features

1. **Domain changes**: Start with models in `domain/models.py`
2. **Port interfaces**: Define contracts in `application/ports/`
3. **Use cases**: Implement business logic in `application/usecases/`
4. **Adapters**: Technical implementations in `infrastructure/`
5. **Interface**: Update CLI in `interfaces/cli/main.py` (no business logic!)

### Testing Strategy

- **Unit tests**: Domain models and use cases
- **Integration tests**: Full pipeline with real images (V2+)
- **Schema tests**: JSON output validation (mandatory)

### Code Quality

- Type annotations on all functions
- No business logic in CLI
- No direct library imports in domain/application
- All public APIs documented with docstrings

## License

MIT

