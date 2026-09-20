# JalRakshak AI — Machine Learning Methodology & Risk Scoring Engine

## Risk Score Formula
Composite community-level water-borne disease risk indicator:

\[
R = 100 \times (0.25 S + 0.25 W + 0.20 E + 0.15 H + 0.10 V + 0.05 A)
\]

### Risk Components (Normalized 0 to 1):
- **S (Symptom/Health Risk)**: Scaled reported disease cases.
- **W (Water Quality Risk)**: IS 10500 drinking water standard deviation (pH [6.5-8.5], TDS [500], NO3 [45], F [1.5], Fe [1.0]).
- **E (Environmental/Rainfall Risk)**: Z-score normalized monsoon rainfall surplus.
- **H (Historical Risk)**: Region-specific historical vulnerability weighting.
- **V (Vulnerability Baseline)**: Population density & infrastructure exposure index.
- **A (Abnormal Pattern Risk)**: Anomaly score from Isolation Forest.

### Prototype Risk Bands
- `0–30`: LOW
- `31–50`: MODERATE
- `51–70`: HIGH
- `71–85`: VERY HIGH
- `86–100`: CRITICAL

## Machine Learning Models
1. **Logistic Regression Baseline**: Standard linear model for binary high-risk classification baseline.
2. **Random Forest Classifier**: Main prototype ensemble model trained on multi-parameter environmental/health features.
3. **Isolation Forest Anomaly Detector**: Unsupervised anomaly detection flagging abnormal environmental patterns ("Abnormal pattern detected").

## Technical Honesty & Non-Fabrication Rule
If ground-truth labels are absent on real public source data, the system reports:
`"Insufficient labelled data for reliable supervised model evaluation."`
Supervised precision/recall/F1 metrics are evaluated strictly on synthetic demo datasets.
