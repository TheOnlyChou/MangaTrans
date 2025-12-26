"""OCR port interface.

Defines the contract for OCR engines without coupling to any specific implementation.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from mangatrans.domain.models import TextRegion


class OCRPort(ABC):
    """Abstract interface for OCR engines."""

    @abstractmethod
    def detect_text(self, image_path: Path, source_lang: str) -> List[TextRegion]:
        """
        Detect text regions in an image.

        Args:
            image_path: Path to the image file
            source_lang: Source language code (e.g., "ja", "ko")

        Returns:
            List of detected text regions with coordinates and raw text
        """
        pass

    @abstractmethod
    def get_engine_info(self) -> tuple[str, str]:
        """
        Get engine name and version.

        Returns:
            Tuple of (engine_name, version)
        """
        pass