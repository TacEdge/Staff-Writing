"""Side-by-side visual comparison: DFI 5.1 figure pages vs rendered output.

    python -m staffwriting.compare            (writes output/comparisons/*.png)

DFI pages are rendered from source/dfi-5.1/dfi_5_1.pdf into reference/dfi-pages/.
Note the DFI figures are scaled down inside a frame, so compare layout and
proportions, not absolute size.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from . import REPO_ROOT

DFI_PDF = REPO_ROOT / "source" / "dfi-5.1" / "dfi_5_1.pdf"
DFI_PAGES = REPO_ROOT / "reference" / "dfi-pages"
OUT = REPO_ROOT / "output" / "comparisons"

# name -> (DFI PDF pages, rendered PDF, rendered pages)
PAIRS = {
    "annex-1a": ([49, 50, 51, 52, 53], "output/annex-1a/1a-classified.pdf", [1, 2, 2, 3, 4]),
    "minute-2c-example": ([70, 71], "output/minute/2c-example.pdf", [1, 2]),
    "minute-2d-template": ([72, 73], "output/minute/2d-structure.pdf", [1, 2]),
    "submission-2e-example": ([74, 75], "output/submission/2e-example.pdf", [1, 2]),
    "submission-2f-template": ([76, 77], "output/submission/2f-structure.pdf", [1, 2]),
    "dpb-2o-template": ([100], "output/dpb/2o-structure.pdf", [1]),
    "vr-2p-example": ([104, 105, 106], "output/visit-report/2p-example.pdf", [1, 2, 3]),
    "vr-2q-template": ([107, 109], "output/visit-report/2q-structure.pdf", [1, 3]),
    "internal-letter-2g-example": ([83], "output/internal-letter/2g-example.pdf", [1]),
    "internal-letter-2h-typed": ([84], "output/internal-letter/2h-typed-structure.pdf", [1]),
    "internal-letter-2h-handwritten": ([85], "output/internal-letter/2h-handwritten-congratulatory.pdf", [1]),
    "external-letter-2i-example": ([86], "output/external-letter/2i-example.pdf", [1]),
    "external-letter-2j-typed": ([87], "output/external-letter/2j-typed-structure.pdf", [1]),
    "external-letter-2j-handwritten": ([88], "output/external-letter/2j-handwritten.pdf", [1]),
}


def dfi_page(n: int, dpi: int = 70) -> Path:
    DFI_PAGES.mkdir(parents=True, exist_ok=True)
    png = DFI_PAGES / f"dfi-p{n:03d}.png"
    if not png.exists():
        prefix = DFI_PAGES / f"tmp-{n}"
        subprocess.run(["pdftoppm", "-f", str(n), "-l", str(n), "-r", str(dpi), "-png",
                        str(DFI_PDF), str(prefix)], check=True)
        next(DFI_PAGES.glob(f"tmp-{n}*.png")).rename(png)
    return png


def out_page(pdf: Path, n: int, dpi: int = 70) -> Image.Image:
    prefix = OUT / "tmp"
    subprocess.run(["pdftoppm", "-f", str(n), "-l", str(n), "-r", str(dpi), "-png", str(pdf), str(prefix)], check=True)
    p = next(OUT.glob("tmp*.png"))
    im = Image.open(p).copy()
    p.unlink()
    return im


def pair_image(left: Image.Image, right: Image.Image, title_l: str, title_r: str) -> Image.Image:
    h = max(left.height, right.height) + 24
    c = Image.new("RGB", (left.width + right.width + 20, h), "white")
    c.paste(left, (0, 24))
    c.paste(right, (left.width + 20, 24))
    d = ImageDraw.Draw(c)
    d.text((8, 4), title_l, fill="black")
    d.text((left.width + 28, 4), title_r, fill="black")
    return c


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (dfi_pages, rendered, out_pages) in PAIRS.items():
        pdf = REPO_ROOT / rendered
        for i, (dp, op) in enumerate(zip(dfi_pages, out_pages), start=1):
            left = Image.open(dfi_page(dp))
            right = out_page(pdf, op)
            img = pair_image(left, right, f"DFI 5.1 PDF p{dp}", f"Rendered {Path(rendered).name} p{op} (LibreOffice preview, Carlito)")
            img.save(OUT / f"{name}-{i}.png")
            print(OUT / f"{name}-{i}.png")


if __name__ == "__main__":
    main()
