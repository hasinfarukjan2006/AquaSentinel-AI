import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def calculate_water_quality_risk(row):
    """
    Computes normalized water quality risk score W (0 to 1) based on IS 10500 drinking water standards.
    Standard limits:
    - pH: 6.5 to 8.5
    - TDS: 500 mg/L (acceptable), 2000 mg/L (max)
    - NO3: 45 mg/L
    - F: 1.5 mg/L
    - Fe: 1.0 mg/L
    """
    deviations = []
    
    # pH
    ph = row.get('ph')
    if pd.notna(ph):
        if ph < 6.5:
            deviations.append(min((6.5 - ph) / 2.0, 1.0))
        elif ph > 8.5:
            deviations.append(min((ph - 8.5) / 2.0, 1.0))
        else:
            deviations.append(0.0)
            
    # TDS
    tds = row.get('tds_mg_l')
    if pd.notna(tds):
        if tds > 500:
            deviations.append(min((tds - 500) / 1500.0, 1.0))
        else:
            deviations.append(0.0)
            
    # Nitrate NO3
    no3 = row.get('no3_mg_l')
    if pd.notna(no3):
        if no3 > 45:
            deviations.append(min((no3 - 45) / 55.0, 1.0))
        else:
            deviations.append(0.0)
            
    # Fluoride F
    f = row.get('f_mg_l')
    if pd.notna(f):
        if f > 1.5:
            deviations.append(min((f - 1.5) / 2.0, 1.0))
        else:
            deviations.append(0.0)

    # Iron Fe
    fe = row.get('fe_mg_l')
    if pd.notna(fe):
        if fe > 1.0:
            deviations.append(min((fe - 1.0) / 3.0, 1.0))
        else:
            deviations.append(0.0)

    if not deviations:
        return 0.2  # Default baseline risk when unmeasured
    
    return float(np.clip(np.mean(deviations), 0.0, 1.0))

def compute_risk_components(df):
    """
    Applies Prototype Risk Score Formula:
    R = 100 * (0.25*S + 0.25*W + 0.20*E + 0.15*H + 0.10*V + 0.05*A)
    """
    # 1. Symptom / Community Health Risk (S)
    h_vals = df['health_value'].fillna(0)
    h_max = h_vals.max() if h_vals.max() > 0 else 1.0
    S = (h_vals / h_max).clip(0.0, 1.0)

    # 2. Water Quality Risk (W)
    W = df.apply(calculate_water_quality_risk, axis=1)

    # 3. Environmental / Rainfall Risk (E)
    rf_vals = df['rainfall_mm'].fillna(df['rainfall_mm'].median() if df['rainfall_mm'].median() > 0 else 100.0)
    rf_mean = rf_vals.mean() if len(rf_vals) > 0 else 100.0
    rf_std = rf_vals.std() if len(rf_vals) > 1 and rf_vals.std() > 0 else 50.0
    
    # Rainfall Z-Score & Risk
    rf_zscore = (rf_vals - rf_mean) / rf_std
    df['rainfall_anomaly'] = rf_zscore.round(2)
    df['rainfall_change'] = ((rf_vals - rf_mean) / rf_mean * 100).round(2)
    
    # High excess rainfall increases environmental risk
    E = (0.5 + 0.25 * rf_zscore).clip(0.0, 1.0)

    # 4. Historical Risk (H)
    H = pd.Series([0.3] * len(df))
    if 'district' in df.columns:
        dist_counts = df['district'].value_counts()
        high_risk_dists = ['Salem', 'Chennai', 'Visakhapatnam', 'Kamrup Metropolitan', 'Guntur']
        H = df['district'].apply(lambda d: 0.65 if d in high_risk_dists else 0.25)

    # 5. Vulnerability Risk (V)
    # Population density / sanitation baseline estimate per district
    V = pd.Series([0.35] * len(df))

    # 6. Abnormal Pattern Risk (A) - Isolation Forest Anomaly Score
    feature_cols = ['ph', 'ec_us_cm', 'tds_mg_l', 'no3_mg_l', 'rainfall_mm']
    df_feat = df[feature_cols].copy()
    for col in feature_cols:
        df_feat[col] = df_feat[col].fillna(df_feat[col].median() if df_feat[col].median() is not np.nan else 0.0)

    iso = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    iso_preds = iso.fit_predict(df_feat)
    iso_scores = -iso.decision_function(df_feat) # Higher score = more anomalous
    
    # Normalize A between 0 and 1
    score_min, score_max = iso_scores.min(), iso_scores.max()
    if score_max > score_min:
        A = (iso_scores - score_min) / (score_max - score_min)
    else:
        A = np.zeros(len(df))
        
    df['anomaly_score'] = iso_scores.round(3)
    df['abnormal_pattern_flag'] = (iso_preds == -1).astype(int)

    # Calculate Total Prototype Risk Score R
    R = 100.0 * (0.25 * S + 0.25 * W + 0.20 * E + 0.15 * H + 0.10 * V + 0.05 * A)
    R = R.round(1).clip(0.0, 100.0)

    df['risk_score'] = R
    df['health_risk_component'] = S.round(2)
    df['water_risk_component'] = W.round(2)
    df['env_risk_component'] = E.round(2)
    df['hist_risk_component'] = H.round(2)
    df['vuln_risk_component'] = V.round(2)
    df['abnormal_risk_component'] = A.round(2)

    # Categorize Risk Class
    def get_risk_class(score):
        if score <= 30.0:
            return 'LOW'
        elif score <= 50.0:
            return 'MODERATE'
        elif score <= 70.0:
            return 'HIGH'
        elif score <= 85.0:
            return 'VERY HIGH'
        else:
            return 'CRITICAL'

    df['risk_class'] = df['risk_score'].apply(get_risk_class)
    return df

def feature_engineering():
    processed_dir = 'data/processed'
    derived_dir = 'data/derived'

    # Process Integrated Real Dataset
    real_path = os.path.join(processed_dir, 'JalRakshak_Integrated_Dataset.csv')
    if os.path.exists(real_path):
        df_real = pd.read_csv(real_path)
        df_real = compute_risk_components(df_real)
        df_real.to_csv(real_path, index=False)
        print(f"Feature engineering complete on Real Dataset ({len(df_real)} records).")

    # Process Synthetic Demo Dataset
    demo_path = os.path.join(processed_dir, 'JalRakshak_Synthetic_Demo_Dataset.csv')
    demo_path2 = os.path.join(processed_dir, 'synthetic_demo_dataset.csv')
    if os.path.exists(demo_path):
        df_demo = pd.read_csv(demo_path)
        df_demo = compute_risk_components(df_demo)
        df_demo.to_csv(demo_path, index=False)
        df_demo.to_csv(demo_path2, index=False)
        print(f"Feature engineering complete on Synthetic Demo Dataset ({len(df_demo)} records).")

if __name__ == '__main__':
    feature_engineering()
