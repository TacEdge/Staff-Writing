import copy

import pytest
import yaml
from docx import Document
from pydantic import ValidationError

from conftest import FIXTURES
from staffwriting.render import load_template, render_file

BASE = yaml.safe_load(open(FIXTURES / "external-letter" / "2j-typed-structure.yaml"))


def _content(**over):
    d = copy.deepcopy(BASE)
    for k, v in over.items():
        if v is None:
            d.pop(k, None)
        else:
            d[k] = v
    return load_template("external-letter").schema.model_validate(d)


def test_accepts_2j_structure():
    _content()


@pytest.mark.parametrize("over, why", [
    (dict(file_reference="ABC 1"), "no file reference on external letters 2.1.16(6)"),
    (dict(references=["X"]), "reference goes in the introductory paragraph 2.1.16(10)"),
    (dict(close={"mode": "none"}), "greeting without close 2.1.18(9)"),
    (dict(salutation={"mode": "none"}), "close without greeting 2.1.18(9)"),
    (dict(annexes=[{"title": "x"}]), "no annexes 2.1.16(18)"),
    (dict(purpose="routine"), "purpose is an internal-letter field"),
])
def test_rejects(over, why):
    with pytest.raises(ValidationError):
        _content(**over)


def test_warnings():
    w = " ".join(_content(salutation={"mode": "typed", "text": "Dear Sir"}, close={"mode": "typed", "text": "Yours sincerely"},
                          body=[{"para": "We will meet at 1300 hrs. The CO will attend."}]).warnings())
    assert "Yours faithfully" in w           # 2.1.18(4)
    assert "12-hour clock" in w              # 2.1.16(15)
    assert "Check: CO" in w                  # 2.1.16(14)


def test_unnamed_recipient_has_no_greeting_or_close(tmp_path):
    out = tmp_path / "u.docx"
    render_file(FIXTURES / "external-letter" / "variant-unnamed-recipient.yaml", out)
    texts = [p.text for p in Document(str(out)).paragraphs]
    assert not any(t.startswith(("Dear", "Yours")) for t in texts)   # 2.1.18(7), (9)
    assert "GH EXAMPLE" in texts
