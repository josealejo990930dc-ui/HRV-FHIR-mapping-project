import math
import generate_synthetic as g

def comps(b):
    for e in b["entry"]:
        r = e["resource"]
        if r["id"].startswith("hrv-"):
            yield {c["code"]["coding"][0]["code"]: c["valueQuantity"]["value"] for c in r["component"]}

def test_deterministic():
    assert g.patient_bundle(1, 4, 42) == g.patient_bundle(1, 4, 42)
    assert g.patient_bundle(1, 4, 42) != g.patient_bundle(1, 4, 43)

def test_poincare_relations_hold():
    for c in comps(g.patient_bundle(2, 12, 1)):
        assert abs(c["hrv-sd1"] - c["hrv-rmssd"] / math.sqrt(2)) < 0.2  # values are rounded to 1 decimal
        sd2 = math.sqrt(2 * c["112429-6"] ** 2 - (c["hrv-rmssd"] / math.sqrt(2)) ** 2)
        assert abs(c["hrv-sd2"] - sd2) < 0.2  # values are rounded to 1 decimal
        assert abs(c["hrv-lfhf"] - c["hrv-lf-norm"] / c["hrv-hf-norm"]) < 0.02

def test_ranges_and_sofa_total():
    b = g.patient_bundle(3, 24, 5)
    for e in b["entry"]:
        r = e["resource"]
        if r["id"].startswith("map-"): assert 45 <= r["valueQuantity"]["value"] <= 110
        if r["id"].startswith("spo2-"): assert 82 <= r["valueQuantity"]["value"] <= 100
        if r["id"].startswith("sofa-"):
            assert r["valueQuantity"]["value"] == sum(c["valueQuantity"]["value"] for c in r["component"])
