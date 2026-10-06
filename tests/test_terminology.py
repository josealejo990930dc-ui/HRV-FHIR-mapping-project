from conftest import ROOT, load
import generate_synthetic as g

def codings(o, out):
    if isinstance(o, dict):
        if "system" in o and "code" in o and not o["system"].startswith(("http://unitsofmeasure", "http://terminology.hl7.org", "http://hl7.org")):
            out.add((o["system"], o["code"]))
        for v in o.values(): codings(v, out)
    elif isinstance(o, list):
        for v in o: codings(v, out)
    return out

def used():
    s = set()
    for p in (ROOT / "templates").glob("*.json"): codings(load(p.relative_to(ROOT)), s)
    codings(g.patient_bundle(1, 6, 1), s)
    return s

def test_local_codes_defined_in_codesystem():
    defined = {c["code"] for c in load("terminology/CodeSystem-hrv-sepsis.json")["concept"]}
    local = {c for s, c in used() if s == g.LOCAL}
    assert local and local <= defined, local - defined

def test_loinc_codes_in_conceptmap():
    cm = load("terminology/ConceptMap-hrv-sepsis-to-loinc.json")
    mapped = {t["code"] for grp in cm["group"] for el in grp["element"] for t in el.get("target", [])}
    loinc = {c for s, c in used() if s == g.LOINC}
    # codes that are used as Observation.code must be documented in the ConceptMap
    PROFILE_ONLY = {"2708-6"}  # required by the R4 oxygensat profile, not a mapping target (see docs/modeling.md)
    assert loinc - PROFILE_ONLY <= mapped, loinc - PROFILE_ONLY - mapped

def test_rxnorm_codes_present():
    mad = load("templates/MedicationAdministration.json")
    codes = {c["code"] for c in mad["medicationCodeableConcept"]["coding"] if "rxnorm" in c["system"]}
    assert codes == {"7512", "2475337"}

def test_local_displays_match_codesystem():
    disp = {c["code"]: c["display"] for c in load("terminology/CodeSystem-hrv-sepsis.json")["concept"]}
    bad = []
    def walk(o):
        if isinstance(o, dict):
            if o.get("system") == g.LOCAL and "display" in o and disp.get(o["code"]) != o["display"]:
                bad.append((o["code"], o["display"]))
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for p in (ROOT / "templates").glob("*.json"): walk(load(p.relative_to(ROOT)))
    walk(g.patient_bundle(1, 6, 1))
    assert not bad, bad

def test_ig_resources_in_sync():
    for f in (ROOT / "terminology").glob("*.json"):
        assert (ROOT / "input" / "resources" / f.name).read_text() == f.read_text(), f.name
