# JalRakshak AI — REST API Endpoints

Base URL: `http://localhost:5000/api`

| Endpoint | Method | Query Parameters | Description |
|---|---|---|---|
| `/health` | GET | None | System health check and disclaimer |
| `/summary` | GET | `data_type` | Dashboard summary KPIs and risk distribution |
| `/locations` | GET | `data_type` | List of monitored districts and coordinates |
| `/risk` | GET | `data_type`, `district`, `state`, `risk_class`, `limit` | Tabular risk score entries |
| `/risk/<location>` | GET | `data_type` | Detailed location profile, score drivers & verification actions |
| `/water-quality` | GET | `data_type`, `district` | CGWB water quality measurement parameters |
| `/rainfall` | GET | `data_type` | Monsoon rainfall series and Z-scores |
| `/health-data` | GET | `data_type` | Reported water-borne disease case entries |
| `/risk/predict` | POST | JSON Record Payload | Predicts risk score & class using Scikit-Learn model |
| `/alerts` | GET | `data_type`, `level` | Early warning alert decision-support triggers |
| `/data-quality` | GET | None | Data profiling metrics & completeness audit |
| `/model/status` | GET | None | ML model pipeline status and scikit-learn evaluation metrics |
