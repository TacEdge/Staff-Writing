"""Date formatting per 1.2.10 and register A-01/A-02."""

from __future__ import annotations

MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTHS_FULL = ["January", "February", "March", "April", "May", "June", "July", "August",
               "September", "October", "November", "December"]


def abbreviated(d) -> str:
    """dd Mmm yy without a leading zero (2.1.11(2), A-01). Day omitted when it
    is to be handwritten (A-02)."""
    core = f"{MONTHS_SHORT[d.month - 1]} {d.year % 100:02d}"
    return f"{d.day} {core}" if d.day else core


def full(d) -> str:
    core = f"{MONTHS_FULL[d.month - 1]} {d.year}"
    return f"{d.day} {core}" if d.day else core
