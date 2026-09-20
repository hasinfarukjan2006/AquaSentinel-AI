# JalRakshak AI — Demonstration Guide
**Tagline:** "From Water Risk to Early Action."

## One-Command Demo Quickstart
To launch the full JalRakshak AI working software prototype on a Windows machine:

1. Double-click or run:
   ```cmd
   run_demo.bat
   ```
2. The batch launcher will:
   - Initialize the SQLite database `database/jalrakshak.db`
   - Start the Flask REST API backend on `http://localhost:5000`
   - Launch the React frontend dashboard on `http://localhost:5173`

## Key Pages to Demonstrate
1. **Login Portal**: Role selection (Health Official, Admin, Field Worker, Viewer).
2. **Main Dashboard**: Real-time KPI cards, Risk Distribution bar chart, High-Risk locations, Interactive Leaflet map, and System Status.
3. **Data Mode Switcher (Header)**:
   - Toggle **Demo Mode (Interactive)** to inspect 520 multi-indicator synthetic records with complete overlap.
   - Toggle **Real Public Source Data** to inspect strict preserved CGWB 2024, IMD 1901-2021, and Rajya Sabha health data.
4. **Risk Monitoring & Location Profile**: Search for **Salem**, **Chennai**, or **Visakhapatnam** to view score driver breakdowns and recommended verification actions.
5. **Water Quality & Health Pages**: Inspect actual CGWB parameters and official Rajya Sabha case numbers with explicit disclaimers.
6. **Data Explorer**: Test filtering and CSV export.
7. **Model Status & Data Quality**: Inspect Scikit-Learn model metrics, Isolation Forest score, and data engineering completeness.
