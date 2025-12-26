"""Port interfaces for external dependencies."""
from .ocr import OCRPort
from .translator import TranslatorPort

__all__ = ["OCRPort", "TranslatorPort"]