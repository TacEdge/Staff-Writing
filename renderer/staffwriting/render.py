"""Load a template (templates/<id>/template.yaml + schema.py), validate the
content file against it, and build the .docx."""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import TEMPLATES_DIR, blocks, tokens
from .builder import Builder


@dataclass
class Template:
    id: str
    spec: dict
    schema: object  # pydantic model class `Content`


@dataclass
class Result:
    path: Path
    warnings: list[str] = field(default_factory=list)
    spec: dict = field(default_factory=dict)
    margins: str = "standard"


def load_template(template_id: str) -> Template:
    folder = TEMPLATES_DIR / template_id
    with open(folder / "template.yaml", encoding="utf-8") as fh:
        spec = yaml.safe_load(fh)
    mod_spec = importlib.util.spec_from_file_location(f"sw_template_{template_id.replace('-', '_')}", folder / "schema.py")
    mod = importlib.util.module_from_spec(mod_spec)
    sys.modules[mod_spec.name] = mod  # pydantic resolves postponed annotations via sys.modules
    mod_spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return Template(template_id, spec, mod.Content)


def load_content(path: Path):
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    tpl = load_template(data["type"])
    content = tpl.schema.model_validate(data)
    return tpl, content


def build(tpl: Template, content, out: Path) -> Result:
    tk = tokens.load()
    page = tpl.spec.get("page", {})
    # A content file may select an alternative margin variant where DFI allows
    # one (eg the 4 cm right margin for briefs, 1.2.16(2), 2.2.7(1)).
    margins = getattr(content, "margins", None) or page.get("margins", "standard")
    b = Builder(
        tk, content.markings,
        copy=getattr(content, "copy_number", None),
        draft=bool(getattr(content, "draft", None)),
        draft_medium=getattr(content, "draft", None) or "electronic",
        margins=margins,
        orientation=page.get("orientation", "portrait"),
        page_regime=page.get("numbering", "standard"),
    )
    b.date_style = tpl.spec.get("date", {}).get("style", "abbreviated")
    b.warnings.extend(content.warnings() if hasattr(content, "warnings") else [])
    for entry in tpl.spec["blocks"]:
        name, opts = (entry, {}) if isinstance(entry, str) else next(iter(entry.items()))
        blocks.REGISTRY[name](b, content, opts or {})
    out.parent.mkdir(parents=True, exist_ok=True)
    b.save(out)
    return Result(out, b.warnings, tpl.spec, margins)


def render_file(content_path: Path, out: Path) -> Result:
    tpl, content = load_content(content_path)
    return build(tpl, content, out)
