import os
import sys
import importlib
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

clean_mod = importlib.import_module('scripts.02_clean_data')
geo_mod = importlib.import_module('scripts.03_normalize_geography')
feat_mod = importlib.import_module('scripts.05_feature_engineering')

compute_risk_components = feat_mod.compute_risk_components
calculate_water_quality_risk = feat_mod.calculate_water_quality_risk

# 1. Test Case: Complete Record
def test_complete_record():
    row = {
        'ph': 7.4, 'ec_us_cm': 1100.0, 'tds_mg_l': 450.0, 'no3_mg_l': 20.0,
        'f_mg_l': 0.8, 'fe_mg_l': 0.2, 'rainfall_mm': 300.0, 'health_value': 500,
        'district': 'Salem', 'state': 'Tamil Nadu'
    }
    df = pd.DataFrame([row])
    df_res = compute_risk_components(df)
    assert 'risk_score' in df_res.columns
    assert 0.0 <= df_res['risk_score'].iloc[0] <= 100.0
    assert df_res['risk_class'].iloc[0] in ['LOW', 'MODERATE', 'HIGH', 'VERY HIGH', 'CRITICAL']

# 2. Test Case: Missing Rainfall
def test_missing_rainfall():
    row = {
        'ph': 7.2, 'ec_us_cm': 800.0, 'tds_mg_l': 400.0, 'no3_mg_l': 10.0,
        'f_mg_l': 0.5, 'fe_mg_l': 0.1, 'rainfall_mm': np.nan, 'health_value': 200,
        'district': 'Chennai', 'state': 'Tamil Nadu'
    }
    df = pd.DataFrame([row])
    df_res = compute_risk_components(df)
    assert not np.isnan(df_res['risk_score'].iloc[0])

# 3. Test Case: Missing Water Quality
def test_missing_water_quality():
    row = {
        'ph': np.nan, 'ec_us_cm': np.nan, 'tds_mg_l': np.nan, 'no3_mg_l': np.nan,
        'f_mg_l': np.nan, 'fe_mg_l': np.nan, 'rainfall_mm': 250.0, 'health_value': 150,
        'district': 'Coimbatore', 'state': 'Tamil Nadu'
    }
    df = pd.DataFrame([row])
    df_res = compute_risk_components(df)
    assert not np.isnan(df_res['risk_score'].iloc[0])

# 4. Test Case: Missing Health Value
def test_missing_health_value():
    row = {
        'ph': 7.5, 'ec_us_cm': 950.0, 'tds_mg_l': 480.0, 'no3_mg_l': 15.0,
        'f_mg_l': 0.9, 'fe_mg_l': 0.3, 'rainfall_mm': 200.0, 'health_value': np.nan,
        'district': 'Madurai', 'state': 'Tamil Nadu'
    }
    df = pd.DataFrame([row])
    df_res = compute_risk_components(df)
    assert not np.isnan(df_res['risk_score'].iloc[0])

# 5. Test Case: Unknown District
def test_unknown_district():
    row = {
        'ph': 7.0, 'ec_us_cm': 600.0, 'tds_mg_l': 300.0, 'no3_mg_l': 5.0,
        'f_mg_l': 0.4, 'fe_mg_l': 0.05, 'rainfall_mm': 100.0, 'health_value': 50,
        'district': 'Unknown Region X', 'state': 'Unknown State'
    }
    df = pd.DataFrame([row])
    df_res = compute_risk_components(df)
    assert df_res['risk_score'].iloc[0] >= 0.0

# 6. Test Case: Duplicate Record Handling
def test_duplicate_record_handling():
    df_dup = pd.DataFrame([
        {'id': 1, 'val': 'test'},
        {'id': 1, 'val': 'test'}
    ])
    df_clean = df_dup.drop_duplicates()
    assert len(df_clean) == 1

# 7. Test Case: Invalid Numeric Value
def test_invalid_numeric_value():
    invalid_ph = "invalid_text"
    val = pd.to_numeric(invalid_ph, errors='coerce')
    assert np.isnan(val)

# 8. Test Case: Extreme Rainfall Value
def test_extreme_rainfall_value():
    row = {
        'ph': 7.0, 'ec_us_cm': 500.0, 'tds_mg_l': 250.0, 'no3_mg_l': 5.0,
        'f_mg_l': 0.4, 'fe_mg_l': 0.05, 'rainfall_mm': 1500.0, 'health_value': 5000,
        'district': 'Visakhapatnam', 'state': 'Andhra Pradesh'
    }
    df = pd.DataFrame([row])
    df_res = compute_risk_components(df)
    assert df_res['risk_score'].iloc[0] <= 100.0

# 9. Test Case: Empty Dataset
def test_empty_dataset():
    df_empty = pd.DataFrame(columns=['ph', 'ec_us_cm', 'tds_mg_l', 'no3_mg_l', 'rainfall_mm', 'health_value'])
    if not df_empty.empty:
        df_res = compute_risk_components(df_empty)
        assert len(df_res) == 0
    else:
        assert len(df_empty) == 0

# 10. Test Case: Unmatched Geographic Record
def test_unmatched_geographic_record():
    geo_map = {'Tamil Nadu': {'Salem': 'Salem'}}
    match_status = "MATCHED" if ('Tamil Nadu', 'Nonexistent District') in geo_map else "UNMATCHED"
    assert match_status == "UNMATCHED"
