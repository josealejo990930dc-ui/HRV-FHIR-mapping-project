import re
from conftest import ROOT

FORBIDDEN = re.compile(r"mimic|itemid|carevue|metavision|physionet", re.I)

def test_no_private_traces_in_public_files():
    bad = []
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT)
        if not p.is_file() or rel.parts[0] in {"private", ".git", ".pytest_cache", "out"} or p.suffix in {".xlsx", ".pyc"}:
            continue
        if rel.parts[:1] == ("tests",) and p.name == "test_public_hygiene.py":
            continue
        if FORBIDDEN.search(p.read_text(encoding="utf-8", errors="ignore")):
            bad.append(str(rel))
    assert not bad, bad
