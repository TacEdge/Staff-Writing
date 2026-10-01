import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "renderer"))

FIXTURES = ROOT / "reference" / "fixtures"
HAS_SOFFICE = shutil.which("soffice") is not None


@pytest.fixture
def tmp_out(tmp_path):
    return tmp_path
