"""Translation port interface.

Defines the contract for translation engines without coupling to any specific implementation.
"""
from abc import ABC, abstractmethod
from typing import List


class TranslatorPort(ABC):
    """Abstract interface for translation engines."""

    @abstractmethod
    def translate_batch(
        self, texts: List[str], source_lang: str, target_lang: str
    ) -> List[str]:
        """
        Translate a batch of texts.

        Args:
            texts: List of text strings to translate
            source_lang: Source language code (e.g., "ja", "ko")
            target_lang: Target language code (e.g., "en", "fr")

        Returns:
            List of translated strings in the same order
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