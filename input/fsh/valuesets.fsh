ValueSet: HrvMetricVS
Id: hrv-metric
Title: "HRV metrics"
Description: "The ten HRV metrics carried as components of the hourly HRV panel. Only SDNN has a LOINC code; the rest are local."
* $LNC#112429-6 "Heart rate variability SDNN [Time]"
* $HRV#hrv-rmssd
* $HRV#hrv-sd1
* $HRV#hrv-sd2
* $HRV#hrv-lf-norm
* $HRV#hrv-hf-norm
* $HRV#hrv-lfhf
* $HRV#hrv-sampen
* $HRV#hrv-apen
* $HRV#hrv-dfa-a1

ValueSet: OutcomeLabelVS
Id: outcome-label
Title: "Prediction outcome labels"
Description: "Outcomes that can be predicted at a 6-hour horizon in the example RiskAssessment."
* $HRV#label-sofa-responder
* $HRV#label-cardio
* $HRV#label-sofa-deterioro
