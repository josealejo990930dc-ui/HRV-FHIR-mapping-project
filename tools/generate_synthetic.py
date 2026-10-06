"""Generates synthetic ICU patients as FHIR R4 transaction Bundles.

All values are drawn from general clinical ranges with a fixed seed. They are NOT calibrated to any real cohort.
Usage: python tools/generate_synthetic.py --n 5 --hours 12 --seed 42 --out out/
"""
import argparse, json, math, pathlib, random
from datetime import datetime, timedelta, timezone

BASE = "https://josealejo990930dc-ui.github.io/HRV-FHIR-mapping-project"
LOCAL = BASE + "/CodeSystem/hrv-sepsis"
LOINC, UCUM = "http://loinc.org", "http://unitsofmeasure.org"
OBS_CAT = "http://terminology.hl7.org/CodeSystem/observation-category"
TEST = [{"system": "http://terminology.hl7.org/CodeSystem/v3-ActReason", "code": "HTEST", "display": "test health data"}]
START = datetime(2026, 1, 1, 8, tzinfo=timezone.utc)

def iso(d): return d.strftime("%Y-%m-%dT%H:%M:%SZ")
def q(v, unit, code): return {"value": v, "unit": unit, "system": UCUM, "code": code}
def loinc(c, d): return {"coding": [{"system": LOINC, "code": c, "display": d}]}
def local(c, d): return {"coding": [{"system": LOCAL, "code": c, "display": d}]}
def spo2_code():
    # HL7 R4 'oxygensat' profile (applied automatically with 59408-5) also requires 2708-6 in the same CodeableConcept.
    c = loinc("59408-5", "Oxygen saturation in Arterial blood by Pulse oximetry")
    c["coding"].append({"system": LOINC, "code": "2708-6", "display": "Oxygen saturation in Arterial blood"}); return c
def cat(c, d): return [{"coding": [{"system": OBS_CAT, "code": c, "display": d}]}]
def clamp(x, lo, hi): return max(lo, min(hi, x))

def hrv_components(r, trend):
    """SD1 = RMSSD/sqrt(2) and SD2 = sqrt(2*SDNN^2 - SD1^2) hold by construction."""
    sdnn = clamp(r.gauss(35 + trend, 8), 8, 120)
    rmssd = clamp(sdnn * r.uniform(0.5, 0.85), 4, 100)
    sd1 = rmssd / math.sqrt(2); sd2 = math.sqrt(2 * sdnn ** 2 - sd1 ** 2)
    lf = round(r.uniform(0.2, 0.6), 2); hf = round(r.uniform(0.08, 0.4), 2)
    return [
        (loinc("112429-6", "Heart rate variability SDNN [Time]"), q(round(sdnn, 1), "ms", "ms")),
        (local("hrv-rmssd", "RMSSD"), q(round(rmssd, 1), "ms", "ms")),
        (local("hrv-sd1", "SD1 (Poincare)"), q(round(sd1, 1), "ms", "ms")),
        (local("hrv-sd2", "SD2 (Poincare)"), q(round(sd2, 1), "ms", "ms")),
        (local("hrv-lf-norm", "LF, normalized per epoch"), q(lf, "1", "1")),
        (local("hrv-hf-norm", "HF, normalized per epoch"), q(hf, "1", "1")),
        (local("hrv-lfhf", "LF/HF ratio"), q(round(lf / hf, 2), "1", "1")),
        (local("hrv-sampen", "Sample entropy (RR)"), q(round(r.uniform(0.6, 2.0), 2), "1", "1")),
        (local("hrv-apen", "Approximate entropy (RR)"), q(round(r.uniform(0.6, 1.5), 2), "1", "1")),
        (local("hrv-dfa-a1", "DFA alpha1 (RR)"), q(round(r.uniform(0.7, 1.5), 2), "1", "1"))]

def patient_bundle(i, hours, seed):
    r = random.Random(f"{seed}-{i}")
    pid, enc, dev = f"synthetic-{i:03d}", f"synthetic-icu-{i:03d}", f"ecg-monitor-{i:03d}"
    P, E, D = f"Patient/{pid}", f"Encounter/{enc}", f"Device/{dev}"
    R = []
    def base(rt, rid): return {"resourceType": rt, "id": rid, "meta": {"tag": TEST}}
    def obs(rid, code, category, when, **kw):
        o = base("Observation", rid)
        o.update(status="final", category=category, code=code, subject={"reference": P}, encounter={"reference": E}, effectiveDateTime=iso(when)); o.update(kw); return o
    p = base("Patient", pid); p.update(gender=r.choice(["female", "male"]), birthDate=f"{r.randint(1935, 1985)}-{r.randint(1,12):02d}-{r.randint(1,28):02d}")
    e = base("Encounter", enc); e.update(status="in-progress", **{"class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"}},
        type=[{"text": "Intensive care unit stay"}], subject={"reference": P}, period={"start": iso(START)})
    d = base("Device", dev); d.update(status="active", deviceName=[{"name": "Bedside patient monitor (synthetic)", "type": "user-friendly-name"}], type={"text": "Bedside monitor, ECG lead II"})
    c = base("Condition", f"sepsis-{i:03d}"); c.update(
        clinicalStatus={"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]},
        verificationStatus={"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed"}]},
        category=[{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-category", "code": "encounter-diagnosis"}]}],
        code={"coding": [{"system": "http://snomed.info/sct", "code": "91302008", "display": "Sepsis (disorder)"},
                         {"system": "http://hl7.org/fhir/sid/icd-10", "code": "A41.9", "display": "Septicaemia, unspecified"}], "text": "Sepsis"},
        subject={"reference": P}, encounter={"reference": E}, onsetDateTime=iso(START))
    R += [p, e, d, c]
    trend = r.choice([-0.8, 0.0, 0.8])  # worsening, stable or improving HRV
    for h in range(hours):
        t = START + timedelta(hours=h)
        o = obs(f"hrv-{i:03d}-h{h:02d}", local("hrv-panel", "Hourly heart rate variability panel"), cat("exam", "Exam"), t,
                device={"reference": D}, method=local("median-of-valid-5min-epochs", "Hourly median of valid 5-minute epochs"),
                component=[{"code": k, "valueQuantity": v} for k, v in hrv_components(r, trend * h)])
        del o["effectiveDateTime"]; o["effectivePeriod"] = {"start": iso(t), "end": iso(t + timedelta(hours=1))}
        R.append(o)
        R.append(obs(f"map-{i:03d}-h{h:02d}", loinc("8478-0", "Mean blood pressure"), cat("vital-signs", "Vital Signs"), t, valueQuantity=q(round(clamp(r.gauss(75, 10), 45, 110)), "mmHg", "mm[Hg]")))
        R.append(obs(f"rr-{i:03d}-h{h:02d}", loinc("9279-1", "Respiratory rate"), cat("vital-signs", "Vital Signs"), t, valueQuantity=q(round(clamp(r.gauss(20, 4), 8, 40)), "breaths/minute", "/min")))
        R.append(obs(f"spo2-{i:03d}-h{h:02d}", spo2_code(), cat("vital-signs", "Vital Signs"), t, valueQuantity=q(round(clamp(r.gauss(95, 3), 82, 100)), "%", "%")))
    for h in range(0, hours, 6):  # lactate every 6 h
        R.append(obs(f"lactate-{i:03d}-h{h:02d}", loinc("32693-4", "Lactate [Moles/volume] in Blood"), cat("laboratory", "Laboratory"), START + timedelta(hours=h), valueQuantity=q(round(clamp(r.gauss(2.5, 1.2), 0.5, 10), 1), "mmol/L", "mmol/L")))
    organs = [("96823-0", "Respiration [Score] SOFA"), ("96824-8", "Coagulation [Score] SOFA"), ("96825-5", "Liver [Score] SOFA"),
              ("96826-3", "Cardiovascular [Score] SOFA"), ("96827-1", "Central nervous system [Score] SOFA"), ("96828-9", "Renal [Score] SOFA")]
    scores = [r.randint(0, 3) for _ in organs]
    R.append(obs(f"sofa-{i:03d}", loinc("96790-1", "SOFA Total Score"), cat("survey", "Survey"), START, valueQuantity=q(sum(scores), "score", "{score}"),
                 component=[{"code": loinc(k, n), "valueQuantity": q(s, "score", "{score}")} for (k, n), s in zip(organs, scores)]))
    return {"resourceType": "Bundle", "id": f"synthetic-bundle-{i:03d}", "meta": {"tag": TEST}, "type": "transaction",
            "entry": [{"fullUrl": f"{BASE}/{x['resourceType']}/{x['id']}", "resource": x, "request": {"method": "PUT", "url": f"{x['resourceType']}/{x['id']}"}} for x in R]}

def main():
    a = argparse.ArgumentParser(); a.add_argument("--n", type=int, default=3); a.add_argument("--hours", type=int, default=12)
    a.add_argument("--seed", type=int, default=42); a.add_argument("--out", default="out")
    x = a.parse_args(); out = pathlib.Path(x.out); out.mkdir(parents=True, exist_ok=True)
    for i in range(1, x.n + 1):
        (out / f"bundle-{i:03d}.json").write_text(json.dumps(patient_bundle(i, x.hours, x.seed), indent=2) + "\n")
    print(f"wrote {x.n} bundles to {out}")

if __name__ == "__main__":
    main()
