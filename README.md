# HRV to FHIR mapping (synthetic)

[![validate](https://github.com/josealejo990930dc-ui/HRV-FHIR-mapping-project/actions/workflows/validate.yml/badge.svg)](https://github.com/josealejo990930dc-ui/HRV-FHIR-mapping-project/actions/workflows/validate.yml)
[![implementation-guide](https://github.com/josealejo990930dc-ui/HRV-FHIR-mapping-project/actions/workflows/ig.yml/badge.svg)](https://github.com/josealejo990930dc-ui/HRV-FHIR-mapping-project/actions/workflows/ig.yml)

How do you represent heart rate variability (HRV), hemodynamics, SOFA scores and vasopressor doses in **FHIR R4** and **LOINC**? This repository answers that for a sepsis prediction setting, with profiles, local terminology, a concept map and synthetic examples.

It is based on work from my master's thesis in Biomedical Informatics. **It is a mapping design only: all data are synthetic, and no real patient data or study results are included.**

**Implementation Guide:** <https://josealejo990930dc-ui.github.io/HRV-FHIR-mapping-project/>

## What I found

- **Only 1 of 10 HRV metrics has a LOINC code.** SDNN maps to `112429-6`. RMSSD, SD1, SD2, LF, HF, LF/HF, sample entropy, approximate entropy and DFA alpha1 have no LOINC term (searched manually in LOINC 2.83), so they live in a [local CodeSystem](terminology/CodeSystem-hrv-sepsis.json).
- **Normalized LF and HF are unitless.** If each spectrum is normalized per epoch, LF and HF are not comparable across epochs. Only the LF/HF ratio keeps its meaning, and the model says so.
- **R4 quirk:** `Observation.derivedFrom` cannot reference a `MedicationAdministration`. The norepinephrine-equivalent dose uses `Observation.focus` instead.
- **R4 quirk:** coding SpO2 with `59408-5` makes the validator apply the `oxygensat` profile, which also requires `2708-6` in the same `code`.
- **Equivalence is explicit.** The [ConceptMap](terminology/ConceptMap-hrv-sepsis-to-loinc.json) records how close each mapping is (exact, exact with a generic code, local).

## What is here

| Path | Content |
|---|---|
| `input/fsh/` | FHIR Shorthand source of the Implementation Guide: 4 profiles, 2 value sets, 8 examples |
| `terminology/` | Local `CodeSystem` (28 concepts, English with Spanish designations) and `ConceptMap` to LOINC and SNOMED CT |
| `templates/` | One synthetic JSON template per resource type |
| `examples/` | A transaction `Bundle` for one synthetic ICU patient |
| `tools/` | Template builder and synthetic data generator |
| `tests/` | 25 pytest tests |
| `docs/` | [Modeling decisions](docs/modeling.md) and the [variable catalog](docs/variable_catalog.md) |

Resources used: `Patient`, `Encounter`, `Device`, `Condition`, `Observation` (panel with `component`), `MedicationAdministration`, `RiskAssessment`.

## Quick start

```bash
pip install -r requirements.txt
pytest -q

# generate synthetic patients (general clinical ranges, fixed seed)
python tools/generate_synthetic.py --n 5 --hours 12 --seed 42 --out out/
```

Validate with the official HL7 validator (needs Java; GitHub Actions does this on every push):

```bash
java -jar validator_cli.jar -version 4.0.1 examples/bundle-synthetic-patient.json templates/*.json
```

Build the Implementation Guide locally (needs [SUSHI](https://fshschool.org/)):

```bash
python tools/sync_ig.py && sushi build .
```

## Terminology versions

LOINC 2.83, SNOMED CT International Edition 2026-10-01, RxNorm (norepinephrine `7512`; example clinical drug `2475337`), ICD-10 `A41.9`, UCUM, FHIR 4.0.1.

## Scope and limits

- Synthetic data only. Values come from general clinical ranges and are not calibrated to any cohort.
- The hourly HRV value is the median of valid 5-minute epochs. The source ECG signal itself is not modeled.
- The vasopressor score is a design example. Not every vasoactive drug is modeled as a resource.
- Local codes are published at this project's URL and are not an official terminology.
- This is not a medical device and not for clinical use.

## License

Code: [MIT](LICENSE). Documentation, terminology and examples: [CC BY 4.0](LICENSE-DOCS.md).

## Citation

See [CITATION.cff](CITATION.cff).
