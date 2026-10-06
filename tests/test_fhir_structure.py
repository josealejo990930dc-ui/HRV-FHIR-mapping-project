import importlib, pathlib
import pytest
from conftest import ROOT, load
import generate_synthetic as g

def parse(res):
    cls = getattr(importlib.import_module(f"fhir.resources.{res['resourceType'].lower()}"), res["resourceType"])
    return cls.parse_obj(res)

TEMPLATES = sorted((ROOT / "templates").glob("*.json"))

@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_template_is_valid_r4_and_tagged(path):
    res = load(path.relative_to(ROOT)); parse(res)
    assert res["meta"]["tag"][0]["code"] == "HTEST"

def test_example_bundle_valid():
    from fhir.resources.bundle import Bundle
    b = load("examples/bundle-synthetic-patient.json"); Bundle.parse_obj(b)
    assert all(e["resource"]["meta"]["tag"][0]["code"] == "HTEST" for e in b["entry"])

def test_generated_bundle_valid_and_references_resolve():
    from fhir.resources.bundle import Bundle
    b = g.patient_bundle(1, 6, 7); Bundle.parse_obj(b)
    ids = {f"{e['resource']['resourceType']}/{e['resource']['id']}" for e in b["entry"]}
    refs = []
    def walk(o):
        if isinstance(o, dict):
            if "reference" in o: refs.append(o["reference"])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(b["entry"]); assert set(refs) <= ids

def test_ned_uses_focus_not_derivedfrom():
    assert "derivedFrom" not in load("templates/Observation-ned.json")
