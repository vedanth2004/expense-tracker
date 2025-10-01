from database.db_manager import create_all
import re

def ensure_tables(engine):
    create_all()

def safe_float(x: str):
    try:
        # accept "1,234.56" or "1234,56"
        s = x.strip().replace(",", "")
        return float(s)
    except Exception:
        return None

_slug_re = re.compile(r"[^a-zA-Z0-9_-]+")

def slugify(s: str) -> str:
    return _slug_re.sub("-", s).strip("-").lower()
