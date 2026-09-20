import os
import json
import pandas as pd
import openpyxl

def profile_data():
    raw_dir = 'data/raw'
    reports_dir = 'data/reports'
    os.makedirs(reports_dir, exist_ok=True)

    profile_results = {}
    csv_rows = []

    # 1. Health Dataset Profile
    health_path = os.path.join(raw_dir, 'RS_Session_256_AU_557_1.csv')
    if os.path.exists(health_path):
        df_health = pd.read_csv(health_path)
        missing_count = int(df_health.isnull().sum().sum())
        total_cells = df_health.shape[0] * df_health.shape[1]
        missing_pct = round((missing_count / total_cells) * 100, 2) if total_cells > 0 else 0.0

        profile_results['Health_Data'] = {
            'source_file': 'RS_Session_256_AU_557_1.csv',
            'rows': len(df_health),
            'columns': df_health.columns.tolist(),
            'column_count': len(df_health.columns),
            'years': ['2019', '2020', '2021'],
            'geographic_coverage': 'National (India Aggregate)',
            'missing_cells': missing_count,
            'missing_percentage': missing_pct,
            'data_types': {col: str(dtype) for col, dtype in df_health.dtypes.items()}
        }
        csv_rows.append({
            'source': 'Health Data (Rajya Sabha)',
            'rows': len(df_health),
            'columns': len(df_health.columns),
            'years': '2019, 2020, 2021',
            'geographic_coverage': 'National',
            'missing_pct': missing_pct,
            'notes': 'Reported cases for 5 key water-borne diseases'
        })

    # 2. Rainfall Dataset Profile
    rainfall_path = os.path.join(raw_dir, 'RF_AI_1901-2021.csv')
    if os.path.exists(rainfall_path):
        df_rf = pd.read_csv(rainfall_path)
        missing_count = int(df_rf.isnull().sum().sum())
        total_cells = df_rf.shape[0] * df_rf.shape[1]
        missing_pct = round((missing_count / total_cells) * 100, 2) if total_cells > 0 else 0.0

        profile_results['Rainfall_Data'] = {
            'source_file': 'RF_AI_1901-2021.csv',
            'rows': len(df_rf),
            'columns': df_rf.columns.tolist(),
            'column_count': len(df_rf.columns),
            'years': f"{df_rf['YEAR'].min()} - {df_rf['YEAR'].max()}",
            'geographic_coverage': 'All-India Monsoon Sub-Divisions',
            'missing_cells': missing_count,
            'missing_percentage': missing_pct,
            'data_types': {col: str(dtype) for col, dtype in df_rf.dtypes.items()}
        }
        csv_rows.append({
            'source': 'Monsoon Rainfall (1901-2021)',
            'rows': len(df_rf),
            'columns': len(df_rf.columns),
            'years': f"{df_rf['YEAR'].min()}-{df_rf['YEAR'].max()}",
            'geographic_coverage': 'All-India',
            'missing_pct': missing_pct,
            'notes': 'Monthly monsoon (JUN, JUL, AUG, SEP) and total (JUN-SEP) in mm'
        })

    # 3. Water Quality Dataset Profile
    wq_path = os.path.join(raw_dir, 'JalRakshak_Water_Quality_Real_Dataset.xlsx')
    if os.path.exists(wq_path):
        xls = pd.ExcelFile(wq_path)
        df_wq = pd.read_excel(xls, sheet_name='Water_Quality_Real')
        missing_count = int(df_wq.isnull().sum().sum())
        total_cells = df_wq.shape[0] * df_wq.shape[1]
        missing_pct = round((missing_count / total_cells) * 100, 2) if total_cells > 0 else 0.0

        profile_results['Water_Quality_Data'] = {
            'source_file': 'JalRakshak_Water_Quality_Real_Dataset.xlsx',
            'sheet_name': 'Water_Quality_Real',
            'rows': len(df_wq),
            'columns': df_wq.columns.tolist(),
            'column_count': len(df_wq.columns),
            'years': str(df_wq['Year'].unique().tolist()),
            'states': df_wq['State_UT'].unique().tolist(),
            'districts_count': int(df_wq['District'].nunique()),
            'missing_cells': missing_count,
            'missing_percentage': missing_pct,
            'data_types': {col: str(dtype) for col, dtype in df_wq.dtypes.items()}
        }
        csv_rows.append({
            'source': 'CGWB Water Quality (2024)',
            'rows': len(df_wq),
            'columns': len(df_wq.columns),
            'years': '2024',
            'geographic_coverage': f"{df_wq['State_UT'].nunique()} States ({', '.join(df_wq['State_UT'].unique())})",
            'missing_pct': missing_pct,
            'notes': f"589 ground water stations across {df_wq['District'].nunique()} districts"
        })

    # Save JSON report
    json_path = os.path.join(reports_dir, 'data_profile.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(profile_results, f, indent=2)

    # Save CSV report
    csv_path = os.path.join(reports_dir, 'data_profile.csv')
    df_profile_csv = pd.DataFrame(csv_rows)
    df_profile_csv.to_csv(csv_path, index=False)

    print(f"Data profiling complete. Saved to:\n  - {json_path}\n  - {csv_path}")

if __name__ == '__main__':
    profile_data()
