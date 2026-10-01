"""LibreOffice preview rendering (register T-04). Carlito stands in for Calibri.

Previews are for checking only; the deliverable is the .docx opened in Word.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def to_pdf(docx: Path) -> Path:
    docx = docx.resolve()
    outdir = docx.parent
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(outdir), str(docx)],
        check=True, capture_output=True, timeout=180,
    )
    pdf = outdir / (docx.stem + ".pdf")
    if not pdf.exists():
        raise RuntimeError(f"LibreOffice did not produce {pdf} (is libreoffice-writer installed?)")
    return pdf


def to_png(pdf: Path, outprefix: Path, dpi: int = 80) -> list[Path]:
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(outprefix)], check=True)
    return sorted(outprefix.parent.glob(outprefix.name + "-*.png"))
