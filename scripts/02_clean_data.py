import os
import pandas as pd
import numpy as np

def clean_data():
    raw_dir = 'data/raw'
    derived_dir = 'data/derived'
    os.makedirs(derived_dir, exist_ok=True)

    # 1. Clean Health Data
    health_path = os.path.join(raw_dir, 'RS_Session_256_AU_557_1.csv')
    if os.path.exists(health_path):
        df_h = pd.read_csv(health_path)
        # Strip string columns
        for col in df_h.columns:
            if df_h[col].dtype == 'object':
                df_h[col] = df_h[col].astype(str).str.strip()
        
        # Ensure numbers are numeric
        for year_col in ['No. of Cases Reported - 2019', 'No. of Cases Reported - 2020', 'No. of Cases Reported - 2021']:
            df_h[year_col] = pd.to_numeric(df_h[year_col], errors='coerce')
        
        # Deduplicate
        df_h = df_h.drop_duplicates()
        df_h.to_csv(os.path.join(derived_dir, 'cleaned_health.csv'), index=False)
        print(f"Cleaned Health Data: {len(df_h)} records")

    # 2. Clean Rainfall Data
    rainfall_path = os.path.join(raw_dir, 'RF_AI_1901-2021.csv')
    if os.path.exists(rainfall_path):
        df_rf = pd.read_csv(rainfall_path)
        # Strip strings
        for col in df_rf.columns:
            if df_rf[col].dtype == 'object':
                df_rf[col] = df_rf[col].astype(str).str.strip()
        
        # Convert numeric
        numeric_cols = ['YEAR', 'JUN', 'JUL', 'AUG', 'SEP', 'JUN-SEP']
        for col in numeric_cols:
            df_rf[col] = pd.to_numeric(df_rf[col], errors='coerce')
        
        # Validate rainfall values (must be >= 0)
        for col in ['JUN', 'JUL', 'AUG', 'SEP', 'JUN-SEP']:
            df_rf.loc[df_rf[col] < 0, col] = np.nan
        
        df_rf = df_rf.drop_duplicates()
        df_rf.to_csv(os.path.join(derived_dir, 'cleaned_rainfall.csv'), index=False)
        print(f"Cleaned Rainfall Data: {len(df_rf)} records")

    # 3. Clean Water Quality Data
    wq_path = os.path.join(raw_dir, 'JalRakshak_Water_Quality_Real_Dataset.xlsx')
    if os.path.exists(wq_path):
        df_wq = pd.read_excel(wq_path, sheet_name='Water_Quality_Real')
        
        # Strip string columns
        for col in df_wq.select_dtypes(include=['object']).columns:
            df_wq[col] = df_wq[col].astype(str).str.strip()
        
        # Convert measurement columns to numeric
        param_cols = ['pH', 'EC_uS_cm', 'TDS_mg_L', 'Cl_mg_L', 'NO3_mg_L', 'SO4_mg_L',
                      'F_mg_L', 'Total_Hardness_mg_L', 'Fe_mg_L', 'As_ppb', 'U_ppb',
                      'Mn_mg_L', 'Cu_mg_L', 'Pb_mg_L', 'Zn_mg_L', 'Ni_mg_L', 'Cd_mg_L', 'Cr_mg_L']
        
        for col in param_cols:
            if col in df_wq.columns:
                df_wq[col] = pd.to_numeric(df_wq[col], errors='coerce')
        
        # Validate physical parameter bounds
        if 'pH' in df_wq.columns:
            df_wq.loc[(df_wq['pH'] < 0) | (df_wq['pH'] > 14), 'pH'] = np.nan
        
        # Negative concentration check
        for col in param_cols:
            if col in df_wq.columns and col != 'pH':
                df_wq.loc[df_wq[col] < 0, col] = np.nan
        
        # Deduplicate
        df_wq = df_wq.drop_duplicates()
        df_wq.to_csv(os.path.join(derived_dir, 'cleaned_water_quality.csv'), index=False)
        print(f"Cleaned Water Quality Data: {len(df_wq)} records")

if __name__ == '__main__':
    clean_data()
