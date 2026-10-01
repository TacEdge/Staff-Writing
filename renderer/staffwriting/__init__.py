"""DFI 5.1 staff-writing renderer.

Every formatting value comes from standards/spec/dfi-5.1-tokens.yaml (see
tokens.py). Document types live in templates/<id>/ (template.yaml + schema.py).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS_PATH = REPO_ROOT / "standards" / "spec" / "dfi-5.1-tokens.yaml"
TEMPLATES_DIR = REPO_ROOT / "templates"
