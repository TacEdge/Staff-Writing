"""Regression tests for defects found in the Phase 2 consolidation audit."""

import copy

import pytest
import yaml
from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from pydantic import ValidationError

from conftest import FIXTURES
from staffwriting.letters import date_style_warnings
from staffwriting.lint import lint
from staffwriting.model import Annex, CopyNumber, DocDate, Identifier
from staffwriting.render import load_template, render_file


def _load(kind, name):
    return copy.deepcopy(yaml.safe_load(open(FIXTURES / kind / name)))


def test_invalid_calendar_date_rejected():
    with pytest.raises(ValidationError):
        DocDate(year=2025, month=2, day=31)
    d = _load("visit-report", "2q-structure.yaml")
    d["date"] = {"year": 2025, "month": 2, "day": 30}
    with pytest.raises(ValidationError):          # previously crashed in warnings()
        load_template("visit-report").schema.model_validate(d)


@pytest.mark.parametrize("kind, name, tpl", [
    ("dpb", "2o-structure.yaml", "dpb"),
    ("visit-report", "2q-structure.yaml", "visit-report"),
    ("internal-letter", "2h-typed-structure.yaml", "internal-letter"),
])
def test_copy_number_bound_everywhere(kind, name, tpl):
    d = _load(kind, name)
    d["copy_number"] = {"number": 5, "of": 2}
    with pytest.raises(ValidationError):
        load_template(tpl).schema.model_validate(d)


def test_annex_date_needs_identifier():
    with pytest.raises(ValidationError):
        Annex(title="X", date={"year": 2025, "month": 1, "day": 2})


def test_letter_rejects_distribution():
    d = _load("external-letter", "2j-typed-structure.yaml")
    d["distribution"] = ["A"]
    with pytest.raises(ValidationError):
        load_template("external-letter").schema.model_validate(d)


def test_may_abbreviated_date_flagged():
    assert date_style_warnings(["On 2 May 26 we met."])


def test_identifier_year_is_four_digits():
    with pytest.raises(ValidationError):
        Identifier(number=3, year=25)


def test_dpb_service_not_rendered_warning():
    d = _load("dpb", "2o-structure.yaml")
    d["signature"]["service"] = "Army"
    w = " ".join(load_template("dpb").schema.model_validate(d).warnings())
    assert "Service given is not rendered" in w


def test_lint_flags_hyperlink_in_letter(tmp_path):
    out = tmp_path / "l.docx"
    render_file(FIXTURES / "external-letter" / "2i-example.yaml", out)
    d = Document(str(out))
    d.paragraphs[-1]._p.append(parse_xml(f'<w:hyperlink {nsdecls("w")}><w:r><w:t>x</w:t></w:r></w:hyperlink>'))
    bad = tmp_path / "bad.docx"
    d.save(str(bad))
    msgs = [m for lvl, m in lint(bad, doc_type="external-letter") if lvl == "ERROR"]
    assert any("hyperlinks" in m for m in msgs)
