# FHIR R4 modeling decisions

All resources in `templates/` and `examples/` are **synthetic**. They carry the `HTEST` (test health data) tag and contain no patient data. Probabilities in the `RiskAssessment` are arbitrary placeholders, not model output.

## Resource map

| Concept | FHIR R4 resource | Code system | Template |
|---|---|---|---|
| Patient (synthetic) | `Patient` | n/a | `Patient.json` |
| ICU stay | `Encounter` (class `IMP`) | n/a | `Encounter.json` |
| Bedside monitor | `Device` | n/a | `Device.json` |
| Sepsis | `Condition` | SNOMED CT `91302008`, ICD-10 `A41.9` | `Condition.json` |
| Hourly HRV (10 metrics) | `Observation` panel with one `component` per metric | LOINC `112429-6` (SDNN) + local codes | `Observation-hrv-hourly.json` |
| Mean blood pressure | `Observation` (vital-signs) | LOINC `8478-0` | `Observation-vital-map.json` |
| Respiratory rate | `Observation` (vital-signs) | LOINC `9279-1` | `Observation-vital-rr.json` |
| Pulse oximetry | `Observation` (vital-signs) | LOINC `59408-5` | `Observation-vital-spo2.json` |
| Lactate | `Observation` (laboratory) | LOINC `32693-4` | `Observation-lactate.json` |
| SOFA total + 6 organ scores | `Observation` with 6 `component` | LOINC `96790-1`, `96823-0` to `96828-9` | `Observation-sofa.json` |
| Vasopressor infusion | `MedicationAdministration` | SNOMED CT `45555007`, RxNorm `7512` (ingredient), `2475337` (clinical drug) | `MedicationAdministration.json` |
| Norepinephrine-equivalent dose | `Observation` (therapy), `focus` to the infusion | local `ned` | `Observation-ned.json` |
| Predicted outcomes | `RiskAssessment` (one `prediction` per outcome) | local codes | `RiskAssessment.json` |

A transaction `Bundle` with one synthetic ICU patient is in `examples/bundle-synthetic-patient.json`.

## Design decisions

1. **HRV as one panel Observation per hour.** The ten metrics share a time window, device and method, so they are `component`s of a single Observation. `effectivePeriod` is the hour, `device` points to the monitor, and `method` states that the hourly value is the median of the valid 5-minute epochs.
2. **Only SDNN has a LOINC code.** RMSSD, SD1, SD2, LF, HF, LF/HF, sample entropy, approximate entropy and DFA alpha1 have no LOINC term (searched manually in LOINC 2.83). They use the local `CodeSystem` in `terminology/`. This gap is one of the project's findings.
3. **LF and HF are unitless.** The extraction normalizes each spectrum by its own maximum, so LF and HF are dimensionless per epoch and not comparable across epochs. Only LF/HF keeps its meaning. They carry UCUM `1` and local codes that say `norm`.
4. **Panel score as a SOFA Observation.** `96790-1` holds the total; the six organ scores (`96823-0` to `96828-9`) are components. LOINC's SOFA panel `96789-3` is an order panel, so it is not used as the `Observation.code`.
5. **Mean blood pressure uses the generic code.** The source mixes invasive and non-invasive measurements, so the method-less `8478-0` is used rather than `76214-6` or `76536-2`.
6. **Lactate uses the generic blood code.** `32693-4` does not specify the specimen; the arterial code `2518-9` was rejected on purpose.
7. **R4 reference rule.** In R4, `Observation.derivedFrom` cannot point to a `MedicationAdministration`, so the norepinephrine-equivalent dose uses `Observation.focus`.
8. **Predictions in `RiskAssessment`.** Each outcome is a `prediction` with `probabilityDecimal` and the 6-hour `whenPeriod`. `basis` lists the observations that fed the prediction.
9. **Test-data tag.** Every resource has `meta.tag` `HTEST`.
10. **SpO2 carries two LOINC codes.** `59408-5` is the mapped concept. The HL7 R4 `oxygensat` profile, applied automatically by the validator when it sees `59408-5`, also requires `2708-6` in the same `code`. So `2708-6` is added for profile conformance only. It is not a mapping target and is not in the `ConceptMap`.

## Validation status

- All templates, the bundle, the `CodeSystem` and the `ConceptMap` parse and validate structurally against FHIR R4 (4.0.1) with `fhir.resources` 6.4.0.
- The official HL7 validator (`validator_cli.jar` 6.10.4) runs in GitHub Actions. First run: 1 error (SpO2 profile, fixed in decision 10); the remaining messages are warnings (no terminology server for UCUM, no narrative, no `performer`, which is by design for synthetic data). Run it locally with:

```bash
java -jar validator_cli.jar -version 4.0.1 examples/bundle-synthetic-patient.json templates/*.json
```

## Known gaps

- `Observation.device` and `method` are modeled, but the source ECG signal is not (no `SampledData`).
- Local codes and the `ConceptMap` use the project's GitHub Pages canonical URL; they resolve only once the Implementation Guide is published.
- The medication carries SNOMED CT (substance), RxNorm ingredient `7512` and one RxNorm clinical drug (`2475337`, premixed bag) as an illustrative product. Other vasopressors are not modeled as resources; regional dictionaries are out of scope.
