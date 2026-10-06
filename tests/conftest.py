import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
def load(p): return json.loads((ROOT / p).read_text(encoding="utf-8"))
