import pytest
from pydantic import ValidationError

from staffwriting import dates
from staffwriting.inline import _split_footnotes, plain
from staffwriting.model import DocDate, Markings
from staffwriting.render import load_template


def test_abbreviated_date_no_leading_zero_and_handwritten_day():
    assert dates.abbreviated(DocDate(year=2025, month=6, day=1)) == "1 Jun 25"   # 2.1.11(2), A-01
    assert dates.abbreviated(DocDate(year=2025, month=6)) == "Jun 25"            # A-02
    assert dates.full(DocDate(year=2016, month=9, day=2)) == "2 September 2016"  # 1.2.10b


def test_inline_plain_and_footnotes():
    assert plain("a **note** that *x*^[fn **b**]") == "a note that x"
    assert _split_footnotes("x.^[one [two]] y") == [("text", "x."), ("fn", "one [two]"), ("text", " y")]


def test_markings_order():
    m = Markings(classification="CONFIDENTIAL", endorsement="SENSITIVE")
    assert m.header_lines() == ["CONFIDENTIAL", "SENSITIVE"]     # 1.2.16(5)
    assert m.footer_lines() == ["SENSITIVE", "CONFIDENTIAL"]     # mirror, classification last
    assert Markings(endorsement="IN-CONFIDENCE").warnings()       # 1.1.10f
    with pytest.raises(ValidationError):
        Markings(classification="OFFICIAL")                       # closed vocabulary (A-13)


BASE = dict(type="minute", originator="HQ", date={"year": 2025, "month": 6}, subject="S",
            to=[{"appointment": "CA"}], body=[{"para": "Text."}],
            signature={"initials": "AB", "surname": "C", "rank": "MAJ", "appointment": "SO2"})


def _minute(**over):
    Content = load_template("minute").schema
    return Content.model_validate({**BASE, **over})


def test_minute_schema_accepts_minimal():
    _minute()


@pytest.mark.parametrize("over, why", [
    (dict(to=[]), "action addressee required 2.1.11(5)"),
    (dict(info=[f"X{i}" for i in range(7)]), "max six info addressees 2.1.11(5)"),
    (dict(distribution=["A"]), "distribution replaces addressees 2.1.11(7)"),
    (dict(signature={"initials": "A.B.", "surname": "C", "rank": "MAJ", "appointment": "X"}), "no stops in initials"),
    (dict(signature={"initials": "AB", "surname": "C", "rank": "Maj.", "appointment": "X"}), "no stops in ranks"),
    (dict(body=[{"recommendations": {"lead": "It is recommended that CA:", "items": ["note that x"]}}]), "bold verb 1.2.11(2)"),
    (dict(body=[{"para": {"heading": "Margins.", "text": "x"}}]), "heading full stop is added"),
    (dict(identifier={"number": 3}), "nn/yyyy pair"),
    (dict(unknown_field=1), "unknown fields rejected"),
])
def test_minute_schema_rejects(over, why):
    with pytest.raises(ValidationError):
        _minute(**over)


def test_minute_warnings():
    c = _minute(subject="Mixed case", body=[{"para": "Costs rose 5% (e.g. fuel)!"}])
    w = " ".join(c.warnings())
    for frag in ("upper case", "per cent", "eg, ie, etc", "Exclamation", "Purpose"):
        assert frag in w
