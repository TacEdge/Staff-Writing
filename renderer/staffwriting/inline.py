"""Inline mark-up for content strings.

Supported:
    **bold**   *italic*   __underline__   ^[footnote text]
Footnote text may itself contain bold/italic/underline. Use a backslash to
escape a literal marker (\\* \\_ \\^).

The renderer never rewrites the author's words; it only applies formatting.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from docx.text.paragraph import Paragraph

_TOKEN = re.compile(r"(\\[*_^\[\]]|\*\*|__|\*|\^\[)")


@dataclass
class Fmt:
    bold: bool = False
    italic: bool = False
    underline: bool = False


def _split_footnotes(text: str):
    """Yield ('text', s) and ('fn', s) segments, honouring nested brackets."""
    i, out, buf = 0, [], []
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            buf.append(text[i : i + 2])
            i += 2
            continue
        if text.startswith("^[", i):
            depth, j = 1, i + 2
            while j < len(text) and depth:
                if text[j] == "\\":
                    j += 2
                    continue
                depth += {"[": 1, "]": -1}.get(text[j], 0)
                j += 1
            if depth:
                raise ValueError(f"Unclosed footnote in: {text!r}")
            out.append(("text", "".join(buf)))
            buf = []
            out.append(("fn", text[i + 2 : j - 1]))
            i = j
            continue
        buf.append(text[i])
        i += 1
    out.append(("text", "".join(buf)))
    return [s for s in out if s[1] or s[0] == "fn"]


def _emit_runs(paragraph: Paragraph, text: str, base: Fmt) -> None:
    state = Fmt(base.bold, base.italic, base.underline)
    pos = 0
    for m in _TOKEN.finditer(text):
        if m.start() > pos:
            _run(paragraph, text[pos : m.start()], state)
        tok = m.group(0)
        if tok.startswith("\\"):
            _run(paragraph, tok[1], state)
        elif tok == "**":
            state.bold = not state.bold
        elif tok == "__":
            state.underline = not state.underline
        elif tok == "*":
            state.italic = not state.italic
        pos = m.end()
    if pos < len(text):
        _run(paragraph, text[pos:], state)


def _run(paragraph: Paragraph, s: str, f: Fmt) -> None:
    r = paragraph.add_run(s)
    if f.bold:
        r.bold = True
    if f.italic:
        r.italic = True
    if f.underline:
        r.underline = True


def add_inline(paragraph: Paragraph, text: str, ctx, base: Fmt | None = None) -> None:
    """Append formatted runs (and footnotes) for `text` to `paragraph`.

    ctx must provide .footnotes (ooxml.Footnotes), .fn_text_style and
    .fn_ref_style (style ids).
    """
    base = base or Fmt()
    for kind, seg in _split_footnotes(text):
        if kind == "text":
            _emit_runs(paragraph, seg, base)
        else:
            fn_par = ctx.footnotes.add(paragraph._p, ctx.fn_text_style, ctx.fn_ref_style)
            _emit_runs(fn_par, seg.strip(), Fmt())


def plain(text: str) -> str:
    """Text with mark-up and footnotes removed (for validation and lint)."""
    parts = [seg for kind, seg in _split_footnotes(text) if kind == "text"]
    s = "".join(parts)
    s = re.sub(r"\\([*_^\[\]])", r"\1", re.sub(r"(?<!\\)(\*\*|__|\*)", "", s))
    return s
