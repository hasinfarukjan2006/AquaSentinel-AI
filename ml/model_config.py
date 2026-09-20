import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
MODEL_DIR = os.path.join(BASE_DIR, 'ml', 'models')
REPORT_DIR = os.path.join(BASE_DIR, 'ml', 'reports')

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

FEATURE_COLS = [
    'ph', 'ec_us_cm', 'tds_mg_l', 'cl_mg_l', 'no3_mg_l',
    'so4_mg_l', 'f_mg_l', 'total_hardness_mg_l', 'fe_mg_l',
    'rainfall_mm', 'health_value'
]

TARGET_COL = 'is_high_risk'

RANDOM_STATE = 42

LOGISTIC_PARAMS = {
    'C': 1.0,
    'max_iter': 1000,
    'random_state': RANDOM_STATE
}

RANDOM_FOREST_PARAMS = {
    'n_estimators': 100,
    'max_depth': 8,
    'random_state': RANDOM_STATE
}

ISOLATION_FOREST_PARAMS = {
    'n_estimators': 100,
    'contamination': 0.1,
    'random_state': RANDOM_STATE
}
