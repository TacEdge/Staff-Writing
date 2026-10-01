"""Output baselines for controlled regression comparison.

`snapshot` renders every fixture in reference/fixtures/ and stores, per fixture,
the canonical XML of each word/*.xml part plus the list of embedded media (name,
size, SHA-256). `diff` compares two snapshots part by part. Used to prove that a
baseline update changes only what it is meant to change (eg register BR-06).

    python -m staffwriting.baseline snapshot output/baselines/before
    python -m staffwriting.baseline diff output/baselines/before output/baselines/after
    python -m staffwriting.baseline prove-artwork before after   # BR-06 proof
"""

from __future__ import annotations

import difflib
import hashlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path

from lxml import etree

from . import REPO_ROOT
from .render import render_file

FIXTURES = REPO_ROOT / "reference" / "fixtures"


R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def _canonical(xml: bytes, rid_targets: dict[str, str] | None = None) -> str:
    """C14N XML, one tag per line. Relationship ids (r:id, r:embed) are replaced
    by their targets so that adding a part does not show as a renumbering."""
    root = etree.fromstring(xml)
    if rid_targets is not None:
        for el in root.iter():
            for attr in list(el.attrib):
                if attr.startswith(f"{{{R_NS}}}") and el.attrib[attr] in rid_targets:
                    el.attrib[attr] = "->" + rid_targets[el.attrib[attr]]
        if root.tag == f"{{{PKG_REL_NS}}}Relationships":
            for rel in list(root):
                rel.attrib.pop("Id", None)
            root[:] = sorted(root, key=lambda r: (r.get("Target", ""), r.get("Type", "")))
    return etree.tostring(root, method="c14n").decode("utf-8").replace("><", ">\n<")


def _rid_map(z: zipfile.ZipFile, part: str) -> dict[str, str]:
    d, f = part.rsplit("/", 1)
    rels = f"{d}/_rels/{f}.rels"
    if rels not in z.namelist():
        return {}
    root = etree.fromstring(z.read(rels))
    return {r.get("Id"): r.get("Target") for r in root}


def snapshot(dest: Path) -> list[str]:
    dest.mkdir(parents=True, exist_ok=True)
    names = []
    with tempfile.TemporaryDirectory() as tmp:
        for fx in sorted(FIXTURES.glob("*/*.yaml")):
            key = f"{fx.parent.name}__{fx.stem}"
            out = Path(tmp) / f"{key}.docx"
            render_file(fx, out)
            fdir = dest / key
            fdir.mkdir(exist_ok=True)
            media = {}
            with zipfile.ZipFile(out) as z:
                for n in sorted(z.namelist()):
                    data = z.read(n)
                    if n.startswith("word/media/"):
                        media[n] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                    elif n.endswith(".xml") or n.endswith(".rels"):
                        if n.startswith("docProps/"):
                            continue            # timestamps; not content
                        rmap = _rid_map(z, n) if n.startswith("word/") and n.endswith(".xml") else None
                        if n.endswith(".rels"):
                            rmap = {}
                        (fdir / n.replace("/", "__")).write_text(_canonical(data, rmap))
            (fdir / "_media.json").write_text(json.dumps(media, indent=1, sort_keys=True))
            names.append(key)
    return names


def diff(a: Path, b: Path) -> dict[str, list[str]]:
    """Return {fixture: [unified-diff lines]} for every fixture that differs."""
    result: dict[str, list[str]] = {}
    for fa in sorted(p for p in a.iterdir() if p.is_dir()):
        fb = b / fa.name
        lines: list[str] = []
        if not fb.exists():
            result[fa.name] = ["(missing in second snapshot)"]
            continue
        parts = sorted({p.name for p in fa.iterdir()} | {p.name for p in fb.iterdir()})
        for part in parts:
            ta = (fa / part).read_text().splitlines() if (fa / part).exists() else []
            tb = (fb / part).read_text().splitlines() if (fb / part).exists() else []
            if ta != tb:
                lines += list(difflib.unified_diff(ta, tb, f"a/{part}", f"b/{part}", lineterm="", n=0))
        if lines:
            result[fa.name] = lines
    for fb in sorted(p for p in b.iterdir() if p.is_dir()):
        if not (a / fb.name).exists():
            result[fb.name] = ["(new in second snapshot)"]
    return result


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _without_device_run(text: str, *, picture: bool) -> tuple[str, int]:
    """Remove the letterhead device run: the italic placeholder run (before
    BR-06) or the run holding the inline picture (after)."""
    root = etree.fromstring(text.replace(">\n<", "><").encode())
    removed = 0
    for r in list(root.iter(f"{{{W_NS}}}r")):
        hit = (r.find(f"{{{W_NS}}}drawing") is not None) if picture else (
            "official artwork not held" in "".join(r.itertext()))
        if hit:
            r.getparent().remove(r)
            removed += 1
    return etree.tostring(root, method="c14n").decode(), removed


def prove_artwork_only(a: Path, b: Path) -> tuple[bool, list[str]]:
    """Register BR-06: show that the only change between snapshots a and b is
    the identity artwork (placeholder run -> picture run, plus its image part)."""
    ok, lines = True, []
    for fx, _ in diff(a, b).items():
        fa, fb = a / fx, b / fx
        parts = sorted({p.name for p in fa.iterdir()} | {p.name for p in fb.iterdir()})
        changed = [p for p in parts if not ((fa / p).exists() and (fb / p).exists()
                                            and (fa / p).read_text() == (fb / p).read_text())]
        checks = {}
        for part in changed:
            ta = (fa / part).read_text() if (fa / part).exists() else ""
            tb = (fb / part).read_text() if (fb / part).exists() else ""
            if part == "word__document.xml":
                xa, na = _without_device_run(ta, picture=False)
                xb, nb = _without_device_run(tb, picture=True)
                checks["document: one placeholder run replaced by one picture run, all else identical"] = (
                    na == 1 and nb == 1 and xa == xb)
            elif part == "word___rels__document.xml.rels":
                la, lb = ta.splitlines(), tb.splitlines()
                added = [l for l in lb if l.startswith("<Relationship")]
                before = [l for l in la if l.startswith("<Relationship")]
                new = [l for l in added if l not in before]
                checks["relationships: one image relationship added, none removed"] = (
                    len(added) == len(before) + 1 and len(new) == 1 and "/image" in new[0]
                    and all(l in added for l in before))
            elif part == "[Content_Types].xml":
                new = [l for l in tb.splitlines() if l not in ta.splitlines() and l.startswith("<")]
                checks["content types: PNG default added only"] = (
                    all("png" in l or l == "</Default>" for l in new)
                    and all(l in tb.splitlines() for l in ta.splitlines()))
            elif part == "_media.json":
                media = json.loads(tb)
                sizes = ", ".join(str(v["bytes"]) + " B" for v in media.values())
                checks[f"media: exactly one image ({sizes})"] = (
                    json.loads(ta or "{}") == {} and len(media) == 1)
            else:
                checks[f"unexpected change in {part}"] = False
        good = all(checks.values())
        ok &= good
        lines.append(f"{'PASS' if good else 'FAIL'} {fx}")
        lines += [f"    {'ok  ' if v else 'FAIL'} {k}" for k, v in checks.items()]
    same = sum(1 for p in a.iterdir() if p.is_dir()) - len(diff(a, b))
    lines.append(f"{same} fixture(s) identical in every part; {len(diff(a, b))} changed")
    return ok, lines


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) == 2 and argv[0] == "snapshot":
        print("\n".join(snapshot(Path(argv[1]))))
        return 0
    if len(argv) == 3 and argv[0] == "diff":
        d = diff(Path(argv[1]), Path(argv[2]))
        for k, lines in d.items():
            print(f"=== {k}")
            print("\n".join(lines))
        print(f"{len(d)} fixture(s) differ")
        return 0
    if len(argv) == 3 and argv[0] == "prove-artwork":
        ok, lines = prove_artwork_only(Path(argv[1]), Path(argv[2]))
        print("\n".join(lines))
        return 0 if ok else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
