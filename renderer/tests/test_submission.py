import copy

import pytest
import yaml
from docx import Document
from pydantic import ValidationError

from conftest import FIXTURES, HAS_SOFFICE
from staffwriting.lint import lint
from staffwriting.render import load_template, render_file

BASE = yaml.safe_load(open(FIXTURES / "submission" / "2f-structure.yaml"))


def _content(**over):
    d = copy.deepcopy(BASE)
    for k, v in over.items():
        if v is None:
            d.pop(k, None)
        else:
            d[k] = v
    return load_template("submission").schema.model_validate(d)


def test_accepts_2f_structure():
    _content()


@pytest.mark.parametrize("over, why", [
    (dict(issue=None), "Issue is mandatory 2.1.12b(1)(a)"),
    (dict(recommendations=None), "Recommendation(s) mandatory 2.1.12b(1)(b)"),
    (dict(financial_and_resource_implications=None), "F&R mandatory 2.1.12b(3); A-34"),
    (dict(financial_and_resource_implications="  "), "F&R must state something"),
    (dict(context=[{"para": "No consultation mentioned."}]), "consultation 2.1.12b(2)(e)"),
    (dict(to=[]), "addressee required"),
    (dict(distribution=["A"]), "no distribution field on a submission"),
])
def test_rejects(over, why):
    with pytest.raises(ValidationError):
        _content(**over)


def test_timing_optional_and_omitted_cleanly(tmp_path):
    c = _content(timing=None)
    heads = [getattr(b.para, "heading", None) for b in c.compose_body() if hasattr(b, "para")]
    assert "Timing" not in heads


def test_warnings():
    w = " ".join(_content(to=[{"appointment": "A"}, {"appointment": "B"}],
                          recommendations={"lead": "It is recommended that A:", "items": ["**note** x"]}).warnings())
    assert "only one addressee" in w
    assert "seeks a decision" in w


def test_2f_element_order(tmp_path):
    out = tmp_path / "s.docx"
    render_file(FIXTURES / "submission" / "2f-structure.yaml", out)
    texts = [p.text for p in Document(str(out)).paragraphs if p.text.strip()]
    starts = ["Defence Logistics Command", "COMLOG MINUTE 14/2025", "Nov 25", "CJDS (through COS DLC)",
              "For information", "REPLACEMENT OF THE LINTON FUEL INSTALLATION", "Reference", "Purpose",
              "Issue.", "Recommendations.", "Timing.", "Context", "Content.", "Sections.", "Argument.",
              "Implications.", "Effects.", "Consultation.", "Financial and resource implications.",
              "Summary", "AB EXAMPLE", "DTelN", "Annex", "Enclosure"]
    idx = [next(i for i, t in enumerate(texts) if t.startswith(s)) for s in starts]
    assert idx == sorted(idx)


@pytest.mark.skipif(not HAS_SOFFICE, reason="needs LibreOffice for page count")
def test_length_warning(tmp_path):
    from staffwriting.preview import to_pdf
    out = tmp_path / "long.docx"
    render_file(FIXTURES / "submission" / "variant-long.yaml", out)
    msgs = [m for lvl, m in lint(out, to_pdf(out), doc_type="submission", max_main_pages=4) if lvl == "WARN"]
    assert any("ideally no longer than 4" in m for m in msgs)
