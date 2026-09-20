# JalRakshak AI — Data Dictionary

| Field | Type | Description |
|---|---|---|
| `record_id` | String | Unique identifier for dataset record |
| `state` | String | Standardized state name (e.g. Tamil Nadu, Andhra Pradesh) |
| `district` | String | Standardized district name (e.g. Salem, Visakhapatnam) |
| `year` | Integer | Observation or report year |
| `season` | String | Season (Pre-Monsoon, Monsoon, Post-Monsoon, Annual) |
| `ph` | Float | Water pH value (IS 10500 standard range: 6.5 - 8.5) |
| `ec_us_cm` | Float | Electrical conductivity in µS/cm |
| `tds_mg_l` | Float | Total Dissolved Solids in mg/L |
| `no3_mg_l` | Float | Nitrate concentration in mg/L |
| `f_mg_l` | Float | Fluoride concentration in mg/L |
| `fe_mg_l` | Float | Iron concentration in mg/L |
| `rainfall_mm` | Float | Monsoon rainfall in millimeters |
| `health_value` | Integer | Reported water-borne disease cases |
| `anomaly_score` | Float | Isolation Forest decision function anomaly score |
| `risk_score` | Float | Composite JalRakshak risk score (0 - 100) |
| `risk_class` | String | LOW, MODERATE, HIGH, VERY HIGH, CRITICAL |
| `data_availability_status` | String | COMPLETE, PARTIAL, WATER_ONLY, RAINFALL_ONLY, HEALTH_ONLY |
| `data_type` | String | REAL_PUBLIC_SOURCE or SYNTHETIC_DEMO |
