# HRV to FHIR mapping (synthetic)

This Implementation Guide documents how heart rate variability (HRV), hemodynamic, SOFA and vasopressor variables from a sepsis prediction project map to LOINC and FHIR R4.

**It is a mapping design.** All examples are synthetic and tagged `HTEST`. No patient data and no study results are included.

### Highlights

* Only one of the ten HRV metrics (SDNN) has a LOINC code. The other nine use the project's [local CodeSystem](CodeSystem-hrv-sepsis.html), which documents a terminology gap.
* LF and HF are normalized per epoch, so they are unitless and only the LF/HF ratio is comparable across epochs.
* In FHIR R4, `Observation.derivedFrom` cannot point to a `MedicationAdministration`, so the norepinephrine-equivalent dose uses `Observation.focus`.
* The [ConceptMap](ConceptMap-hrv-sepsis-to-loinc.html) records the equivalence level of every mapping.

See the [Artifacts](artifacts.html) page for profiles, value sets and examples.
