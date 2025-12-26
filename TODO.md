# TODO - Roadmap for V2 and beyond

## V2 - Real OCR + Translation Implementation

### Infrastructure Layer

#### 1. OCR Adapter (EasyOCR)
**File**: `src/mangatrans/infrastructure/adapters/easyocr_adapter.py`

```python
from pathlib import Path
from typing import List
import easyocr
from mangatrans.application.ports.ocr import OCRPort
from mangatrans.domain.models import TextRegion, BBox

class EasyOCRAdapter(OCRPort):
    def __init__(self, languages: List[str]):
        self.reader = easyocr.Reader(languages)
    
    def detect_text(self, image_path: Path, source_lang: str) -> List[TextRegion]:
        # Implement real detection
        pass
    
    def get_engine_info(self) -> tuple[str, str]:
        return ("easyocr", easyocr.__version__)
```

**Tasks**:
- [ ] Create `easyocr_adapter.py` file
- [ ] Implement `detect_text()` with real detection
- [ ] Map EasyOCR coordinates to `BBox`
- [ ] Handle orientation (horizontal/vertical)
- [ ] Extract confidence score
- [ ] Handle errors (invalid image, etc.)

#### 2. Translation Adapter (Argos Translate)
**File**: `src/mangatrans/infrastructure/adapters/argos_adapter.py`

```python
from typing import List
import argostranslate.package
import argostranslate.translate
from mangatrans.application.ports.translator import TranslatorPort

class ArgosTranslatorAdapter(TranslatorPort):
    def __init__(self, source_lang: str, target_lang: str):
        # Install language packages if necessary
        pass
    
    def translate_batch(self, texts: List[str], source_lang: str, target_lang: str) -> List[str]:
        # Implement real translation
        pass
    
    def get_engine_info(self) -> tuple[str, str]:
        return ("argos", "1.0.0")  # Version to retrieve dynamically
```

**Tasks**:
- [ ] Create `argos_adapter.py` file
- [ ] Implement `translate_batch()` with real translation
- [ ] Handle language pack installation
- [ ] Optimize for batch processing (multiple texts at once)
- [ ] Handle translation errors

#### 3. Image Processing
**File**: `src/mangatrans/infrastructure/image_processor.py`

```python
import cv2
from pathlib import Path
from typing import Tuple

def get_image_dimensions(image_path: Path) -> Tuple[int, int]:
    """Returns (width, height) of an image."""
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")
    height, width = img.shape[:2]
    return (width, height)
```

**Tasks**:
- [ ] Create `image_processor.py` file
- [ ] Implement `get_image_dimensions()`
- [ ] Handle image formats (PNG, JPG, etc.)
- [ ] Add image validation

### Application Layer

#### 4. Use Case Update
**File**: `src/mangatrans/application/usecases/translate_page.py`

**Modifications**:
```python
def translate_page(
    image_path: Path,
    source_lang: str,
    target_lang: str,
    ocr_port: OCRPort,  # Now required
    translator_port: TranslatorPort,  # Now required
) -> PageResult:
    import time
    from mangatrans.infrastructure.image_processor import get_image_dimensions
    
    start_time = time.time()
    
    # 1. Get real dimensions
    width, height = get_image_dimensions(image_path)
    
    # 2. OCR
    ocr_start = time.time()
    regions = ocr_port.detect_text(image_path, source_lang)
    ocr_time = int((time.time() - ocr_start) * 1000)
    
    # 3. Translation
    trans_start = time.time()
    raw_texts = [r.raw_text for r in regions]
    translated_texts = translator_port.translate_batch(raw_texts, source_lang, target_lang)
    trans_time = int((time.time() - trans_start) * 1000)
    
    # 4. Update regions with translation
    for region, translated in zip(regions, translated_texts):
        region.translated_text = translated
    
    # 5. Build result
    total_time = int((time.time() - start_time) * 1000)
    
    # ... rest of code
```

**Tasks**:
- [ ] Modify signature (required ports)
- [ ] Add dimension extraction
- [ ] Call real ports
- [ ] Measure timings
- [ ] Update engine versions

### Interface Layer

#### 5. CLI Update
**File**: `src/mangatrans/interfaces/cli/main.py`

**Modifications**:
```python
def main() -> int:
    # ... argparse code ...
    
    # Instantiate adapters
    from mangatrans.infrastructure.adapters.easyocr_adapter import EasyOCRAdapter
    from mangatrans.infrastructure.adapters.argos_adapter import ArgosTranslatorAdapter
    
    ocr_adapter = EasyOCRAdapter(languages=[args.src, 'en'])
    translation_adapter = ArgosTranslatorAdapter(args.src, args.tgt)
    
    # Call use case with adapters
    result = translate_page(
        image_path=args.image,
        source_lang=args.src,
        target_lang=args.tgt,
        ocr_port=ocr_adapter,
        translator_port=translation_adapter,
    )
    
    # ... export code ...
```

**Tasks**:
- [ ] Instantiate adapters
- [ ] Pass adapters to use case
- [ ] Add progress messages (optional)
- [ ] Handle exceptions properly

### Configuration

#### 6. Dependencies
**File**: `pyproject.toml`

```toml
dependencies = [
    "easyocr>=1.7.0",
    "argostranslate>=1.9.0",
    "opencv-python>=4.8.0",
    "torch>=2.0.0",  # Required by EasyOCR
    "numpy>=1.24.0",
]
```

**Tasks**:
- [ ] Add dependencies in `pyproject.toml`
- [ ] Test installation
- [ ] Document system dependencies (CUDA, etc.)

### Tests

#### 7. Integration Tests
**File**: `tests/test_integration.py`

**Tasks**:
- [ ] Create tests with real images
- [ ] Test OCR detection
- [ ] Test translation
- [ ] Test complete pipeline
- [ ] Add test image fixtures

### Documentation

#### 8. Documentation Update
**Tasks**:
- [ ] Update README.md with V2 instructions
- [ ] Document EasyOCR configuration
- [ ] Document Argos language pack installation
- [ ] Add real usage examples
- [ ] Document expected performance

---

## V3 - Advanced Features

### Features

#### 1. Batch Processing
**File**: `src/mangatrans/application/usecases/translate_batch.py`

- [ ] Process multiple pages at once
- [ ] Folder support
- [ ] Possible parallelization
- [ ] Progress bar

#### 2. Output Image Generation
**File**: `src/mangatrans/infrastructure/renderers/image_renderer.py`

- [ ] Mask original text
- [ ] Overlay translated text
- [ ] Respect orientations (vertical/horizontal)
- [ ] Choose appropriate font (manga fonts)

#### 3. Configuration File
**File**: `config.yaml` or `config.toml`

```yaml
ocr:
  engine: easyocr
  languages: [ja, en]
  gpu: true

translation:
  engine: argos
  cache: true

output:
  format: json
  include_image: false
```

- [ ] Config file support
- [ ] CLI override
- [ ] Config validation

#### 4. Web API (FastAPI)
**File**: `src/mangatrans/interfaces/api/main.py`

- [ ] POST endpoint `/translate`
- [ ] Image upload
- [ ] JSON or translated image return
- [ ] Rate limiting
- [ ] OpenAPI documentation

#### 5. Format Support
- [ ] PDF input/output
- [ ] CBZ/CBR (comic book archives)
- [ ] Batch ZIP processing

---

## V4 - UI & Polish

### Features
- [ ] GUI (Tkinter or PyQt)
- [ ] Web interface (React + FastAPI)
- [ ] Drag & drop
- [ ] Preview
- [ ] Manual translation editing
- [ ] Export to different formats

---

## V1 → V2 Migration Checklist

### Before starting V2
- [ ] Read EasyOCR documentation: https://github.com/JaidedAI/EasyOCR
- [ ] Read Argos Translate documentation: https://github.com/argosopentech/argos-translate
- [ ] Test EasyOCR standalone (outside project)
- [ ] Test Argos Translate standalone
- [ ] Understand available language models

### Development
- [ ] Create branch `v2-ocr-translation`
- [ ] Implement adapters one by one
- [ ] Test each adapter in isolation
- [ ] Integrate into use case
- [ ] Test complete pipeline
- [ ] Measure performance

### Validation
- [ ] Test on real manga images
- [ ] Test on Korean manhwa
- [ ] Verify OCR accuracy
- [ ] Verify translation quality
- [ ] Optimize if necessary

### Documentation
- [ ] Update README
- [ ] Document limitations
- [ ] Add troubleshooting
- [ ] Real examples

---

## Known Issues to Anticipate for V2 Based on EasyOCR and Argos Translate Forums

### Performance
- EasyOCR is slow without GPU (~5-10s per page)
- Argos Translate can be slow for long texts
- → Solution: Caching, parallelization

### Quality
- OCR may miss small/blurry text
- Translation can be literal (missing context)
- → Solution: Post-processing, improved models

### Technical
- Memory management (EasyOCR loads heavy models)
- Heavy dependencies (PyTorch, etc.)
- → Solution: Optimized installation, Docker

---

## Resources

### Documentation
- EasyOCR: https://github.com/JaidedAI/EasyOCR
- Argos Translate: https://github.com/argosopentech/argos-translate
- OpenCV: https://docs.opencv.org/

### Alternatives to Consider
- **OCR**: Tesseract, Google Vision API, Azure OCR
- **Translation**: DeepL API, Google Translate API, OpenAI GPT

### Test Datasets
- Manga109: http://www.manga109.org/
- Public manga scan examples / asurascans

---

**Last updated**: December 25, 2025
**Status**: V1 complete | V2 pending development
