"""Load the shared DFI 5.1 tokens and expose typed accessors.

The renderer must not hard-code formatting values; it reads them from here.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import yaml

from . import TOKENS_PATH

TWIPS_PER_CM = 566.929  # 1 cm = 1440/2.54 twips


def cm_to_twips(cm: float) -> int:
    return int(round(cm * TWIPS_PER_CM))


class Tokens:
    def __init__(self, data: dict[str, Any]):
        self.data = data

    def get(self, dotted: str) -> Any:
        node: Any = self.data
        for part in dotted.split("."):
            node = node[part]
        return node

    def value(self, dotted: str) -> Any:
        node = self.get(dotted)
        return node["value"] if isinstance(node, dict) and "value" in node else node

    # Convenience accessors used throughout the renderer.
    @property
    def font_family(self) -> str:
        return self.value("font.family")

    def size(self, key: str) -> float:
        return self.value(f"font.size.{key}")

    def spacing(self, key: str) -> tuple[int, int]:
        node = self.get(f"spacing.{key}")
        return node["before"], node["after"]

    def margins(self, variant: str) -> dict[str, float]:
        return self.get(f"page.margins.{variant}")

    @property
    def a4_cm(self) -> tuple[float, float]:
        a4 = self.get("page.a4_cm")
        return a4["width"], a4["height"]

    @property
    def tab_cm(self) -> float:
        return self.value("page.default_tab_interval")

    @property
    def text_width_cm(self) -> float:
        m = self.margins("standard")
        return self.a4_cm[0] - m["left"] - m["right"]


@lru_cache(maxsize=1)
def load() -> Tokens:
    with open(TOKENS_PATH, encoding="utf-8") as fh:
        return Tokens(yaml.safe_load(fh))
