Profile: HrvHourlyPanel
Parent: Observation
Id: hrv-hourly-panel
Title: "Hourly HRV panel"
Description: "One Observation per hour with the ten HRV metrics as components. The hourly value is the median of the valid 5-minute epochs."
* meta.tag 1..*
* code = $HRV#hrv-panel
* category 1..1
* category = $ObsCat#exam
* subject 1..1
* encounter 1..1
* effective[x] only Period
* effectivePeriod 1..1
* device 1..1
* device only Reference(Device)
* method 1..1
* method = $HRV#median-of-valid-5min-epochs
* value[x] 0..0
* component 10..10
* component ^slicing.discriminator.type = #pattern
* component ^slicing.discriminator.path = "code"
* component ^slicing.rules = #closed
* component contains
    sdnn 1..1 and rmssd 1..1 and sd1 1..1 and sd2 1..1 and lf 1..1 and
    hf 1..1 and lfhf 1..1 and sampen 1..1 and apen 1..1 and dfa 1..1
* component[sdnn].code = $LNC#112429-6
* component[rmssd].code = $HRV#hrv-rmssd
* component[sd1].code = $HRV#hrv-sd1
* component[sd2].code = $HRV#hrv-sd2
* component[lf].code = $HRV#hrv-lf-norm
* component[hf].code = $HRV#hrv-hf-norm
* component[lfhf].code = $HRV#hrv-lfhf
* component[sampen].code = $HRV#hrv-sampen
* component[apen].code = $HRV#hrv-apen
* component[dfa].code = $HRV#hrv-dfa-a1
* component[sdnn].value[x] only Quantity
* component[rmssd].value[x] only Quantity
* component[sd1].value[x] only Quantity
* component[sd2].value[x] only Quantity
* component[lf].value[x] only Quantity
* component[hf].value[x] only Quantity
* component[lfhf].value[x] only Quantity
* component[sampen].value[x] only Quantity
* component[apen].value[x] only Quantity
* component[dfa].value[x] only Quantity
* component[sdnn].valueQuantity = $UCUM#ms
* component[rmssd].valueQuantity = $UCUM#ms
* component[sd1].valueQuantity = $UCUM#ms
* component[sd2].valueQuantity = $UCUM#ms
* component[lf].valueQuantity = $UCUM#1
* component[hf].valueQuantity = $UCUM#1
* component[lfhf].valueQuantity = $UCUM#1
* component[sampen].valueQuantity = $UCUM#1
* component[apen].valueQuantity = $UCUM#1
* component[dfa].valueQuantity = $UCUM#1

Profile: SofaScore
Parent: Observation
Id: sofa-score
Title: "SOFA score"
Description: "SOFA total score with the six organ scores as components (LOINC 96790-1 and 96823-0 to 96828-9)."
* code = $LNC#96790-1
* subject 1..1
* encounter 1..1
* effective[x] only dateTime
* value[x] only Quantity
* valueQuantity 1..1
* valueQuantity = $UCUM#"{score}"
* component 6..6
* component ^slicing.discriminator.type = #pattern
* component ^slicing.discriminator.path = "code"
* component ^slicing.rules = #closed
* component contains
    respiration 1..1 and coagulation 1..1 and liver 1..1 and
    cardiovascular 1..1 and cns 1..1 and renal 1..1
* component[respiration].code = $LNC#96823-0
* component[coagulation].code = $LNC#96824-8
* component[liver].code = $LNC#96825-5
* component[cardiovascular].code = $LNC#96826-3
* component[cns].code = $LNC#96827-1
* component[renal].code = $LNC#96828-9
* component[respiration].value[x] only Quantity
* component[coagulation].value[x] only Quantity
* component[liver].value[x] only Quantity
* component[cardiovascular].value[x] only Quantity
* component[cns].value[x] only Quantity
* component[renal].value[x] only Quantity

Profile: NorepinephrineEquivalentDose
Parent: Observation
Id: ned-observation
Title: "Norepinephrine-equivalent dose"
Description: "Derived vasopressor dose. In R4, Observation.derivedFrom cannot reference MedicationAdministration, so the infusion is linked through Observation.focus."
* code = $HRV#ned
* subject 1..1
* encounter 1..1
* focus 1..*
* focus only Reference(MedicationAdministration)
* value[x] only Quantity
* valueQuantity 1..1
* valueQuantity = $UCUM#ug/kg/min

Profile: HrvRiskAssessment
Parent: RiskAssessment
Id: hrv-risk-assessment
Title: "Risk assessment from HRV features"
Description: "One prediction per outcome with a probability and a time window. The probabilities in the examples are placeholders, not model output."
* subject 1..1
* encounter 1..1
* occurrence[x] only dateTime
* method 1..1
* basis 1..*
* prediction 1..*
* prediction.outcome 1..1
* prediction.outcome from OutcomeLabelVS (required)
* prediction.probability[x] only decimal
* prediction.probabilityDecimal 1..1
* prediction.when[x] only Period
* prediction.whenPeriod 1..1
