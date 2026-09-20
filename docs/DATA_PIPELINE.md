# JalRakshak AI — Data Engineering Pipeline

## Execution Steps
Developers can run the data pipeline sequentially:

```bash
python scripts/01_profile_data.py
python scripts/02_clean_data.py
python scripts/03_normalize_geography.py
python scripts/04_integrate_sources.py
python scripts/05_feature_engineering.py
python scripts/06_generate_reports.py
```

## Raw Sources
1. `JalRakshak_Water_Quality_Real_Dataset.xlsx`: 589 ground water quality sampling records from Central Ground Water Board (CGWB) 2024 Pre-Monsoon report.
2. `RF_AI_1901-2021.csv`: 121 years of All-India monsoon rainfall series (1901–2021).
3. `RS_Session_256_AU_557_1.csv`: Rajya Sabha Unstarred Question No. 557 reported water-borne disease cases in India (2019–2021).

## Merging & Matching Strategy
- Exact match -> Normalized match -> Controlled fuzzy match.
- Geographic standardization maps raw district strings into canonical names (`data/processed/geography_mapping.csv`).
- Missing values preserved as `NaN` / `NULL`. Tracking column `data_availability_status` flags `COMPLETE`, `PARTIAL`, `WATER_ONLY`, `RAINFALL_ONLY`, `HEALTH_ONLY`.

## 10-Sheet Excel Workbook
Generated at `/data/processed/JalRakshak_Integrated_Dataset.xlsx` with sheets:
1. `Integrated_Data`
2. `Health_Data`
3. `Rainfall_Data`
4. `Water_Quality_Data`
5. `Feature_Engineered_Data`
6. `Data_Quality_Report`
7. `Geography_Mapping`
8. `Data_Dictionary`
9. `Source_Provenance`
10. `README`
