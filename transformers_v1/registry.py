from pathlib import Path
from typing import List, Optional

from .bots.base import TransformerBot
from .bots.bumblebee import Bumblebee
from .bots.ironhide import Ironhide
from .bots.jazz import Jazz
from .bots.ratchet import Ratchet

EXTENSION_FORMATS = {
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".csv": "csv",
    ".md": "markdown",
    ".markdown": "markdown",
    ".html": "html",
    ".htm": "html",
    ".py": "python",
}


class NoAutobotAvailable(Exception):
    """Raised when no bot in the fleet can perform the requested transformation."""


class OptimusPrime:
    """Leader of the Autobots -- routes each job to the right transformer."""

    def __init__(self, bots: Optional[List[TransformerBot]] = None):
        self.bots = bots if bots is not None else [Bumblebee(), Ironhide(), Ratchet(), Jazz()]

    def detect_format(self, path: str) -> str:
        suffix = Path(path).suffix.lower()
        try:
            return EXTENSION_FORMATS[suffix]
        except KeyError as exc:
            raise ValueError(f"Cannot detect format for file extension '{suffix}'") from exc

    def find_bot(self, from_format: str, to_format: str) -> TransformerBot:
        for bot in self.bots:
            if bot.supports(from_format, to_format):
                return bot
        available = sorted(f"{f} -> {t}" for bot in self.bots for f, t in bot.conversions)
        raise NoAutobotAvailable(
            f"No Autobot currently transforms {from_format} -> {to_format}. "
            f"Available conversions: {', '.join(available)}"
        )

    def transform(self, content: str, from_format: str, to_format: str) -> str:
        bot = self.find_bot(from_format, to_format)
        return bot.transform(content, from_format, to_format)
