from abc import ABC, abstractmethod
from typing import Iterable, Tuple


class TransformerBot(ABC):
    """Base class for every Autobot in the Transformers-v1 fleet."""

    name: str

    @property
    @abstractmethod
    def conversions(self) -> Iterable[Tuple[str, str]]:
        """Return the (from_format, to_format) pairs this bot can handle."""

    def supports(self, from_format: str, to_format: str) -> bool:
        return (from_format, to_format) in self.conversions

    @abstractmethod
    def transform(self, content: str, from_format: str, to_format: str) -> str:
        """Transform content from from_format to to_format, returning the new content."""
