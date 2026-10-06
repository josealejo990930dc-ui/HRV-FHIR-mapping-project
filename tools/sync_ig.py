"""Copies the hand-maintained terminology JSON into the IG input folder (single source of truth: terminology/)."""
import pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parent.parent
dst = ROOT / "input" / "resources"; dst.mkdir(parents=True, exist_ok=True)
for f in (ROOT / "terminology").glob("*.json"):
    shutil.copyfile(f, dst / f.name)
print("synced", [f.name for f in dst.glob("*.json")])
