# AquaSentinel AI — AI-Powered Community Water-Borne Disease Early Warning System
**Tagline:** "From Water Risk to Early Action."

AquaSentinel AI is a working software prototype designed for authorized public-health officials. It integrates community-health information, rainfall/environmental indicators, ground-water quality measurements, and historical patterns to calculate a community-level water-borne disease risk indicator.

> **Project Disclaimer:**
> AquaSentinel is a prototype decision-support system for community-level early warning. Risk scores are not medical diagnoses and do not confirm disease outbreaks. Results require validation by authorized health professionals and appropriate field or laboratory investigation before action.

---

## 🌟 Key Product Features
- **Defensible Data Integration Pipeline**: Cleanly profiles, standardizes geography (`geography_mapping.csv`), preserves missing values, and generates a 10-sheet Excel workbook (`JalRakshak_Integrated_Dataset.xlsx`).
- **Data Integrity & Non-Fabrication Guarantee**: Strict separation between preserved real public datasets (`REAL_PUBLIC_SOURCE`) and synthetic demonstration datasets (`SYNTHETIC_DEMO`).
- **Prototype Risk Scoring Engine**: Calculates $R = 100(0.25S + 0.25W + 0.20E + 0.15H + 0.10V + 0.05A)$ with 5 risk classification bands (`LOW`, `MODERATE`, `HIGH`, `VERY HIGH`, `CRITICAL`).
- **Machine Learning Pipeline**: Logistic Regression baseline, Random Forest prototype classifier, and Isolation Forest anomaly detector (`"Abnormal pattern detected"`).
- **Flask REST API Backend**: 12 modular REST endpoints backed by an indexed SQLite database (`database/jalrakshak.db`).
- **Professional Engineering Dashboard**: Built with React, Vite, Tailwind CSS, Recharts, and Leaflet interactive map component across 12 dedicated views/pages.
- **Automated Pytest Test Suite**: Covers 10 data pipeline edge cases, risk score calculations, and API contracts.

---

## 📁 Project Folder Structure

```
JalRakshak/
│
├── frontend/                  # React + Vite + Tailwind CSS + Recharts + Leaflet
│   ├── src/
│   │   ├── components/        # Header, Sidebar, RiskBadge, RiskMap, DisclaimerFooter
│   │   ├── pages/             # Dashboard, RiskMonitoring, LocationDetails, WaterQuality, etc.
│   │   └── services/api.js    # API client
│   ├── package.json
│   └── vite.config.js
│
├── backend/                   # Flask REST API Backend
│   ├── app.py                 # Flask server entrypoint (Port 5000)
│   ├── config.py              # Configuration & paths
│   ├── database.py            # SQLite connection manager
│   ├── routes/                # Health, Risk, Data, and Alert API routes
│   └── requirements.txt
│
├── ml/                        # Scikit-Learn Machine Learning Pipeline
│   ├── train.py               # Model training script
│   ├── predict.py             # Inference engine
│   ├── preprocess.py          # Data scaling & imputation
│   ├── features.py             # Feature selection
│   ├── evaluate.py            # Model evaluation metrics
│   ├── models/                # Saved joblib model artifacts
│   └── reports/               # Model evaluation reports (JSON & CSV)
│
├── data/
│   ├── raw/                   # Preserved original datasets (CGWB, IMD, Rajya Sabha)
│   ├── processed/             # Integrated CSV & 10-sheet Excel workbook
│   ├── derived/               # Cleaned intermediate files
│   └── reports/               # Data profile report (data_profile.json & .csv)
│
├── database/
│   ├── jalrakshak.db          # SQLite database
│   └── init_db.py             # Database schema initialization script
│
├── scripts/
│   ├── 01_profile_data.py     # Step 1: Data profiling report generator
│   ├── 02_clean_data.py       # Step 2: Data cleaning & deduplication
│   ├── 03_normalize_geography.py # Step 3: Geographic canonicalization
│   ├── 04_integrate_sources.py# Step 4: Multi-source defensible join & synthetic generator
│   ├── 05_feature_engineering.py # Step 5: Risk formula & Isolation Forest anomaly detection
│   └── 06_generate_reports.py# Step 6: 10-sheet Excel workbook generator
│
├── tests/
│   ├── test_data_pipeline.py  # 10 data pipeline test cases
│   └── test_backend_api.py    # Flask API test suite
│
├── docs/                      # Technical documentation
│   ├── ARCHITECTURE.md
│   ├── DATA_PIPELINE.md
│   ├── API.md
│   ├── ML_METHODOLOGY.md
│   ├── DATA_DICTIONARY.md
│   └── DEMO_GUIDE.md
│
├── run_backend.bat            # Backend batch launcher
├── run_frontend.bat           # Frontend batch launcher
├── run_demo.bat               # One-command full demo launcher
└── README.md
```

---

## 🚀 Quickstart: Running the Application

### Option A: One-Command Demo Launcher (Recommended)
Simply double-click or run from PowerShell/CMD:
```cmd
run_demo.bat
```
This automatically initializes the SQLite database, starts the Flask REST API on `http://localhost:5000`, and opens the React Frontend Dashboard on `http://localhost:5173`.

### Option B: Running Component Services Separately

1. **Run Backend REST API**:
   ```cmd
   python backend/app.py
   ```
2. **Run Frontend Development Server**:
   ```cmd
   cd frontend
   npm run dev
   ```

---

## 🧪 Running Automated Tests

Run the complete test suite covering 10 data pipeline edge cases and API contracts:
```cmd
python -m pytest tests/
```

---

## 📊 Dataset Statistics & Provenance

| Source File | Description | Real Records Processed |
|---|---|---|
| `JalRakshak_Water_Quality_Real_Dataset.xlsx` | CGWB Ground Water Quality 2024 Pre-Monsoon Report (AP, Assam, Arunachal) | 589 |
| `RF_AI_1901-2021.csv` | IMD All-India Monsoon Rainfall Series (1901–2021) | 121 |
| `RS_Session_256_AU_557_1.csv` | Rajya Sabha Unstarred Question No. 557 Water-Borne Disease Reports (2019–2021) | 5 |
| **Total Real Integrated Records** | Preserved in `JalRakshak_Integrated_Dataset.csv` | **713** |
| **Synthetic Demo Dataset** | Multi-indicator interactive demo records (`synthetic_demo_dataset.csv`) | **520** |

---

## 📄 License & Team
Developed by the JalRakshak Student Software Engineering Team for public-health technology innovation.
