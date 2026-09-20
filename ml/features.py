import pandas as pd
import numpy as np

def prepare_ml_features(df):
    """
    Extracts numerical features and derives target label for supervised classification.
    Target label is_high_risk: 1 if risk_score > 50.0 else 0.
    """
    df_clean = df.copy()
    if 'risk_score' in df_clean.columns:
        df_clean['is_high_risk'] = (df_clean['risk_score'] > 50.0).astype(int)
    else:
        df_clean['is_high_risk'] = 0
    return df_clean
