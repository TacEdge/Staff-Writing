"""CLI:  python -m staffwriting render CONTENT.yaml -o OUT.docx [--pdf] [--lint]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pydantic import ValidationError

from .render import render_file


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="staffwriting")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render", help="validate content and render a .docx")
    r.add_argument("content", type=Path)
    r.add_argument("-o", "--out", type=Path, required=True)
    r.add_argument("--pdf", action="store_true", help="also produce a LibreOffice PDF preview")
    r.add_argument("--lint", action="store_true", help="run structural lint on the output")
    args = ap.parse_args(argv)

    try:
        res = render_file(args.content, args.out)
    except ValidationError as e:
        print(f"Content does not meet the template schema:\n{e}", file=sys.stderr)
        return 2
    print(f"Wrote {res.path}")
    for w in res.warnings:
        print(f"  WARNING: {w}")
    rc = 0
    pdf = None
    if args.pdf or args.lint:
        from .preview import to_pdf
        pdf = to_pdf(res.path)
        print(f"Preview {pdf}")
    if args.lint:
        from .lint import lint
        lint_opts = res.spec.get("lint", {})
        findings = lint(res.path, pdf, doc_type=res.spec.get("id", "minute"),
                        max_main_pages=lint_opts.get("max_main_pages"), margins=res.margins)
        for level, msg in findings:
            print(f"  LINT {level}: {msg}")
        rc = 1 if any(level == "ERROR" for level, _ in findings) else 0
    return rc


if __name__ == "__main__":
    sys.exit(main())
