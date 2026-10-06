"""Builds the synthetic FHIR R4 example resources and bundle. All values are invented."""
import json, math, pathlib
BASE = "https://josealejo990930dc-ui.github.io/HRV-FHIR-mapping-project"
RXN = "http://www.nlm.nih.gov/research/umls/rxnorm"
LOCAL = BASE + "/CodeSystem/hrv-sepsis"
ROOT = pathlib.Path(__file__).resolve().parent.parent
LOINC, UCUM, SCT = "http://loinc.org", "http://unitsofmeasure.org", "http://snomed.info/sct"
OBS_CAT = "http://terminology.hl7.org/CodeSystem/observation-category"
TEST = [{"system": "http://terminology.hl7.org/CodeSystem/v3-ActReason", "code": "HTEST", "display": "test health data"}]
PAT, ENC, DEV = "Patient/synthetic-001", "Encounter/synthetic-icu-001", "Device/ecg-monitor-001"
T0 = "2026-01-01T20:00:00Z"

def q(v, unit, code): return {"value": v, "unit": unit, "system": UCUM, "code": code}
def loinc(c, d): return {"coding": [{"system": LOINC, "code": c, "display": d}]}
def local(c, d): return {"coding": [{"system": LOCAL, "code": c, "display": d}]}
def spo2_code():
    # HL7 R4 'oxygensat' profile (applied automatically with 59408-5) also requires 2708-6 in the same CodeableConcept.
    c = loinc("59408-5", "Oxygen saturation in Arterial blood by Pulse oximetry")
    c["coding"].append({"system": LOINC, "code": "2708-6", "display": "Oxygen saturation in Arterial blood"}); return c
def cat(c, d): return [{"coding": [{"system": OBS_CAT, "code": c, "display": d}]}]
def base(rt, rid): return {"resourceType": rt, "id": rid, "meta": {"tag": TEST}}
def obs(rid, code, category, **kw):
    o = base("Observation", rid); o.update(status="final", category=category, code=code, subject={"reference": PAT}, encounter={"reference": ENC}); o.update(kw); return o

R = {}
R["Patient"] = base("Patient", "synthetic-001"); R["Patient"].update(gender="female", birthDate="1958-03-14")
R["Encounter"] = base("Encounter", "synthetic-icu-001"); R["Encounter"].update(
    status="in-progress", **{"class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "IMP", "display": "inpatient encounter"}},
    type=[{"text": "Intensive care unit stay"}], subject={"reference": PAT}, period={"start": "2026-01-01T08:00:00Z"})
R["Device"] = base("Device", "ecg-monitor-001"); R["Device"].update(status="active", deviceName=[{"name": "Bedside patient monitor (synthetic)", "type": "user-friendly-name"}], type={"text": "Bedside monitor, ECG lead II"})
R["Condition"] = base("Condition", "sepsis-001"); R["Condition"].update(
    clinicalStatus={"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]},
    verificationStatus={"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed"}]},
    category=[{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-category", "code": "encounter-diagnosis"}]}],
    code={"coding": [{"system": SCT, "code": "91302008", "display": "Sepsis (disorder)"},
                     {"system": "http://hl7.org/fhir/sid/icd-10", "code": "A41.9", "display": "Septicaemia, unspecified"}], "text": "Sepsis"},
    subject={"reference": PAT}, encounter={"reference": ENC}, onsetDateTime="2026-01-01T08:00:00Z")

def hrv(h):  # one hourly HRV observation; relations between metrics are kept physiologically consistent
    sdnn = 32.0 + 2 * h; rmssd = 24.0 + h
    sd1 = rmssd / math.sqrt(2); sd2 = math.sqrt(2 * sdnn**2 - sd1**2)
    lf, hf = 0.35, 0.18 - 0.01 * h
    start = f"2026-01-01T{8+h:02d}:00:00Z"; end = f"2026-01-01T{9+h:02d}:00:00Z"
    comp = [
        (loinc("112429-6", "Heart rate variability SDNN [Time]"), q(round(sdnn, 1), "ms", "ms")),
        (local("hrv-rmssd", "RMSSD"), q(round(rmssd, 1), "ms", "ms")),
        (local("hrv-sd1", "SD1 (Poincare)"), q(round(sd1, 1), "ms", "ms")),
        (local("hrv-sd2", "SD2 (Poincare)"), q(round(sd2, 1), "ms", "ms")),
        (local("hrv-lf-norm", "LF, normalized per epoch"), q(lf, "1", "1")),
        (local("hrv-hf-norm", "HF, normalized per epoch"), q(round(hf, 2), "1", "1")),
        (local("hrv-lfhf", "LF/HF ratio"), q(round(lf / hf, 2), "1", "1")),
        (local("hrv-sampen", "Sample entropy (RR)"), q(1.4, "1", "1")),
        (local("hrv-apen", "Approximate entropy (RR)"), q(1.1, "1", "1")),
        (local("hrv-dfa-a1", "DFA alpha1 (RR)"), q(1.05, "1", "1"))]
    o = obs(f"hrv-001-h{h:02d}", local("hrv-panel", "Hourly heart rate variability panel"), cat("exam", "Exam"),
            effectivePeriod={"start": start, "end": end}, device={"reference": DEV},
            method=local("median-of-valid-5min-epochs", "Hourly median of valid 5-minute epochs"),
            component=[{"code": c, "valueQuantity": v} for c, v in comp])
    return o
R["Observation-hrv-hourly"] = hrv(0)
R["Observation-vital-map"] = obs("map-001", loinc("8478-0", "Mean blood pressure"), cat("vital-signs", "Vital Signs"), effectiveDateTime=T0, valueQuantity=q(78, "mmHg", "mm[Hg]"))
R["Observation-vital-rr"] = obs("rr-001", loinc("9279-1", "Respiratory rate"), cat("vital-signs", "Vital Signs"), effectiveDateTime=T0, valueQuantity=q(20, "breaths/minute", "/min"))
R["Observation-vital-spo2"] = obs("spo2-001", spo2_code(), cat("vital-signs", "Vital Signs"), effectiveDateTime=T0, valueQuantity=q(94, "%", "%"))
R["Observation-lactate"] = obs("lactate-001", loinc("32693-4", "Lactate [Moles/volume] in Blood"), cat("laboratory", "Laboratory"), effectiveDateTime=T0, valueQuantity=q(2.8, "mmol/L", "mmol/L"))
sofa = [("96823-0", "Respiration [Score] SOFA", 2), ("96824-8", "Coagulation [Score] SOFA", 1), ("96825-5", "Liver [Score] SOFA", 0),
        ("96826-3", "Cardiovascular [Score] SOFA", 1), ("96827-1", "Central nervous system [Score] SOFA", 1), ("96828-9", "Renal [Score] SOFA", 1)]
R["Observation-sofa"] = obs("sofa-001", loinc("96790-1", "SOFA Total Score"), cat("survey", "Survey"), effectiveDateTime=T0,
    valueQuantity=q(sum(s[2] for s in sofa), "score", "{score}"), component=[{"code": loinc(c, d), "valueQuantity": q(v, "score", "{score}")} for c, d, v in sofa])
R["MedicationAdministration"] = base("MedicationAdministration", "norepi-001"); R["MedicationAdministration"].update(
    status="in-progress", medicationCodeableConcept={"coding": [{"system": SCT, "code": "45555007", "display": "Norepinephrine"}, {"system": RXN, "code": "7512", "display": "norepinephrine"}, {"system": RXN, "code": "2475337", "display": "250 ML norepinephrine 0.016 MG/ML Injection"}], "text": "Norepinephrine infusion"},
    subject={"reference": PAT}, context={"reference": ENC}, effectiveDateTime="2026-01-01T12:00:00Z",
    dosage={"rateQuantity": q(0.08, "ug/kg/min", "ug/kg/min")})
R["Observation-ned"] = obs("ned-001", local("ned", "Norepinephrine equivalent dose"), cat("therapy", "Therapy"), effectiveDateTime=T0,
    valueQuantity=q(0.08, "ug/kg/min", "ug/kg/min"), focus=[{"reference": "MedicationAdministration/norepi-001"}])
pred = lambda c, d, p: {"outcome": local(c, d), "probabilityDecimal": p, "whenPeriod": {"start": T0, "end": "2026-01-02T02:00:00Z"}}
R["RiskAssessment"] = base("RiskAssessment", "response-6h-001"); R["RiskAssessment"].update(
    status="final", method=local("synthetic-example-model", "Synthetic example model (not a real model)"),
    subject={"reference": PAT}, encounter={"reference": ENC}, occurrenceDateTime=T0,
    basis=[{"reference": "Observation/hrv-001-h00"}, {"reference": "Observation/map-001"}, {"reference": "Observation/lactate-001"}, {"reference": "Observation/sofa-001"}],
    prediction=[pred("label-sofa-responder", "SOFA response", 0.62), pred("label-cardio", "Cardiovascular response", 0.48), pred("label-sofa-deterioro", "SOFA deterioration >=2 points", 0.07)],
    note=[{"text": "Synthetic example. Probabilities are arbitrary values, not model output."}])

(ROOT / "templates").mkdir(exist_ok=True); (ROOT / "examples").mkdir(exist_ok=True)
for name, res in R.items():
    (ROOT / "templates" / f"{name}.json").write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n")
entries = [R["Patient"], R["Encounter"], R["Device"], R["Condition"], hrv(0), hrv(1), hrv(2), R["Observation-vital-map"], R["Observation-vital-rr"],
           R["Observation-vital-spo2"], R["Observation-lactate"], R["Observation-sofa"], R["MedicationAdministration"], R["Observation-ned"], R["RiskAssessment"]]
bundle = {"resourceType": "Bundle", "id": "synthetic-bundle-001", "meta": {"tag": TEST}, "type": "transaction",
          "entry": [{"fullUrl": f"{BASE}/{e['resourceType']}/{e['id']}", "resource": e, "request": {"method": "PUT", "url": f"{e['resourceType']}/{e['id']}"}} for e in entries]}
(ROOT / "examples" / "bundle-synthetic-patient.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n")
print(len(R), "templates,", len(entries), "bundle entries")
