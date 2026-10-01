"""Identity artwork (badges and logos) derived from the controlled source.

Register BR-01: the only copy of the artwork is the NZDF Visual Identity
Standards PDF in `source/nzdf-visual-identity/`. Each device is rendered from
its vector original, unaltered, at render time (poppler `pdftocairo`) into a
git-ignored cache. The source checksum is verified before any use.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

from . import REPO_ROOT

MANIFEST = REPO_ROOT / "source" / "nzdf-visual-identity" / "derived" / "artwork-manifest.yaml"
CACHE = Path(os.environ.get("STAFFWRITING_CACHE", REPO_ROOT / "output" / ".cache")) / "artwork"


class ArtworkError(RuntimeError):
    pass


@dataclass(frozen=True)
class Device:
    key: str
    kind: str            # "badge" | "logo"
    page: int
    box: tuple[float, float, float, float]   # x, y, w, h in PDF points
    label: str


@lru_cache(maxsize=1)
def _manifest() -> dict:
    with open(MANIFEST, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def devices() -> dict[str, Device]:
    m = _manifest()
    return {k: Device(k, v["kind"], v["page"], tuple(v["box"]), v["label"]) for k, v in m["devices"].items()}


DEVICE_KEYS = tuple(yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))["devices"])


@lru_cache(maxsize=1)
def _verified_source() -> Path:
    m = _manifest()
    src = REPO_ROOT / m["source"]
    if not src.exists():
        raise ArtworkError(f"Identity source not found: {src}")
    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    if digest != m["sha256"]:
        raise ArtworkError(
            f"Identity source checksum changed ({digest}); expected {m['sha256']}. "
            "Stop: the controlled source has changed (source/nzdf-visual-identity/SOURCE.md)."
        )
    return src


def path(key: str, tk) -> Path:
    """PNG (transparent background) for device `key`, rendered from the source
    so that it carries `identity.render_dpi` pixels per inch at its display size."""
    dev = devices()[key]
    src = _verified_source()
    sha8 = _manifest()["sha256"][:8]
    _, h_cm = size_cm(key, tk)
    dpi = round(tk.value("identity.render_dpi") * (h_cm / 2.54) / (dev.box[3] / 72))
    out = CACHE / f"{key}-{sha8}-{dpi}.png"
    if out.exists():
        return out
    if shutil.which("pdftocairo") is None:
        raise ArtworkError("pdftocairo (poppler-utils) is required to render identity artwork.")
    CACHE.mkdir(parents=True, exist_ok=True)
    x, y, w, h = (round(v * dpi / 72) for v in dev.box)
    stem = out.with_suffix("")
    subprocess.run(
        ["pdftocairo", "-png", "-transp", "-singlefile", "-r", str(dpi),
         "-f", str(dev.page), "-l", str(dev.page),
         "-x", str(x), "-y", str(y), "-W", str(w), "-H", str(h), str(src), str(stem)],
        check=True, capture_output=True,
    )
    if not out.exists():
        raise ArtworkError(f"Artwork render produced no file for {key}.")
    return out


def size_cm(key: str, tk) -> tuple[float, float]:
    """Display width and height (BR-05): height from the DFI figures; a logo is
    never narrower than the VIS minimum width."""
    dev = devices()[key]
    aspect = dev.box[2] / dev.box[3]
    if dev.kind == "badge":
        h = tk.value("identity.badge_height")
        return h * aspect, h
    h = tk.value("identity.logo_height")
    w = h * aspect
    min_w = tk.value("identity.logo_min_width")
    if w < min_w:
        w, h = min_w, min_w / aspect
    return w, h
