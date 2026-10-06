Instance: synthetic-001
InstanceOf: Patient
Usage: #example
Title: "Synthetic patient"
* meta.tag = $ActReason#HTEST
* gender = #female
* birthDate = "1958-03-14"

Instance: synthetic-icu-001
InstanceOf: Encounter
Usage: #example
Title: "Synthetic ICU stay"
* meta.tag = $ActReason#HTEST
* status = #in-progress
* class = http://terminology.hl7.org/CodeSystem/v3-ActCode#IMP "inpatient encounter"
* type.text = "Intensive care unit stay"
* subject = Reference(synthetic-001)
* period.start = "2026-01-01T08:00:00Z"

Instance: ecg-monitor-001
InstanceOf: Device
Usage: #example
Title: "Synthetic bedside monitor"
* meta.tag = $ActReason#HTEST
* status = #active
* deviceName.name = "Bedside patient monitor (synthetic)"
* deviceName.type = #user-friendly-name
* type.text = "Bedside monitor, ECG lead II"

Instance: norepi-001
InstanceOf: MedicationAdministration
Usage: #example
Title: "Synthetic norepinephrine infusion"
* meta.tag = $ActReason#HTEST
* status = #in-progress
* medicationCodeableConcept.coding[0] = $SCT#45555007 "Norepinephrine"
* medicationCodeableConcept.coding[+] = $RXN#7512 "norepinephrine"
* medicationCodeableConcept.coding[+] = $RXN#2475337 "250 ML norepinephrine 0.016 MG/ML Injection"
* medicationCodeableConcept.text = "Norepinephrine infusion"
* subject = Reference(synthetic-001)
* context = Reference(synthetic-icu-001)
* effectiveDateTime = "2026-01-01T12:00:00Z"
* dosage.rateQuantity = 0.08 'ug/kg/min' "ug/kg/min"

Instance: hrv-001-h00
InstanceOf: HrvHourlyPanel
Usage: #example
Title: "Synthetic hourly HRV panel"
* meta.tag = $ActReason#HTEST
* status = #final
* category = $ObsCat#exam
* code = $HRV#hrv-panel "Hourly heart rate variability panel"
* subject = Reference(synthetic-001)
* encounter = Reference(synthetic-icu-001)
* effectivePeriod.start = "2026-01-01T08:00:00Z"
* effectivePeriod.end = "2026-01-01T09:00:00Z"
* device = Reference(ecg-monitor-001)
* method = $HRV#median-of-valid-5min-epochs "Hourly median of valid 5-minute epochs"
* component[sdnn].code = $LNC#112429-6 "Heart rate variability SDNN [Time]"
* component[sdnn].valueQuantity = 32.0 'ms' "ms"
* component[rmssd].code = $HRV#hrv-rmssd "RMSSD"
* component[rmssd].valueQuantity = 24.0 'ms' "ms"
* component[sd1].code = $HRV#hrv-sd1 "SD1 (Poincare)"
* component[sd1].valueQuantity = 17.0 'ms' "ms"
* component[sd2].code = $HRV#hrv-sd2 "SD2 (Poincare)"
* component[sd2].valueQuantity = 41.9 'ms' "ms"
* component[lf].code = $HRV#hrv-lf-norm "LF, normalized per epoch"
* component[lf].valueQuantity = 0.35 '1' "1"
* component[hf].code = $HRV#hrv-hf-norm "HF, normalized per epoch"
* component[hf].valueQuantity = 0.18 '1' "1"
* component[lfhf].code = $HRV#hrv-lfhf "LF/HF ratio"
* component[lfhf].valueQuantity = 1.94 '1' "1"
* component[sampen].code = $HRV#hrv-sampen "Sample entropy (RR)"
* component[sampen].valueQuantity = 1.4 '1' "1"
* component[apen].code = $HRV#hrv-apen "Approximate entropy (RR)"
* component[apen].valueQuantity = 1.1 '1' "1"
* component[dfa].code = $HRV#hrv-dfa-a1 "DFA alpha1 (RR)"
* component[dfa].valueQuantity = 1.05 '1' "1"

Instance: sofa-001
InstanceOf: SofaScore
Usage: #example
Title: "Synthetic SOFA score"
* meta.tag = $ActReason#HTEST
* status = #final
* category = $ObsCat#survey
* code = $LNC#96790-1 "SOFA Total Score"
* subject = Reference(synthetic-001)
* encounter = Reference(synthetic-icu-001)
* effectiveDateTime = "2026-01-01T20:00:00Z"
* valueQuantity = 6 '{score}' "score"
* component[respiration].code = $LNC#96823-0 "Respiration [Score] SOFA"
* component[respiration].valueQuantity = 2 '{score}' "score"
* component[coagulation].code = $LNC#96824-8 "Coagulation [Score] SOFA"
* component[coagulation].valueQuantity = 1 '{score}' "score"
* component[liver].code = $LNC#96825-5 "Liver [Score] SOFA"
* component[liver].valueQuantity = 0 '{score}' "score"
* component[cardiovascular].code = $LNC#96826-3 "Cardiovascular [Score] SOFA"
* component[cardiovascular].valueQuantity = 1 '{score}' "score"
* component[cns].code = $LNC#96827-1 "Central nervous system [Score] SOFA"
* component[cns].valueQuantity = 1 '{score}' "score"
* component[renal].code = $LNC#96828-9 "Renal [Score] SOFA"
* component[renal].valueQuantity = 1 '{score}' "score"

Instance: ned-001
InstanceOf: NorepinephrineEquivalentDose
Usage: #example
Title: "Synthetic norepinephrine-equivalent dose"
* meta.tag = $ActReason#HTEST
* status = #final
* category = $ObsCat#therapy
* code = $HRV#ned "Norepinephrine equivalent dose"
* subject = Reference(synthetic-001)
* encounter = Reference(synthetic-icu-001)
* effectiveDateTime = "2026-01-01T20:00:00Z"
* valueQuantity = 0.08 'ug/kg/min' "ug/kg/min"
* focus = Reference(norepi-001)

Instance: response-6h-001
InstanceOf: HrvRiskAssessment
Usage: #example
Title: "Synthetic risk assessment"
* meta.tag = $ActReason#HTEST
* status = #final
* method = $HRV#synthetic-example-model "Synthetic example model (not a real model)"
* subject = Reference(synthetic-001)
* encounter = Reference(synthetic-icu-001)
* occurrenceDateTime = "2026-01-01T20:00:00Z"
* basis[0] = Reference(hrv-001-h00)
* basis[+] = Reference(sofa-001)
* prediction[0].outcome = $HRV#label-sofa-responder "SOFA response"
* prediction[=].probabilityDecimal = 0.62
* prediction[=].whenPeriod.start = "2026-01-01T20:00:00Z"
* prediction[=].whenPeriod.end = "2026-01-02T02:00:00Z"
* prediction[+].outcome = $HRV#label-sofa-deterioro "SOFA deterioration >=2 points"
* prediction[=].probabilityDecimal = 0.07
* prediction[=].whenPeriod.start = "2026-01-01T20:00:00Z"
* prediction[=].whenPeriod.end = "2026-01-02T02:00:00Z"
* note.text = "Synthetic example. Probabilities are arbitrary values, not model output."
