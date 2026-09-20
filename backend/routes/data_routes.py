import os
import pandas as pd
from flask import Blueprint, jsonify, request
from backend.config import PROCESSED_DIR
from backend.database import query_db

data_bp = Blueprint('data', __name__)

@data_bp.route('/api/locations', methods=['GET'])
def get_locations():
    data_type = request.args.get('data_type', 'REAL_PUBLIC_SOURCE')
    locations = query_db("""
        SELECT r.state, r.district, AVG(l.latitude) as latitude, AVG(l.longitude) as longitude,
               MAX(r.risk_score) as latest_risk_score, MAX(r.risk_class) as latest_risk_class
        FROM risk_scores r
        LEFT JOIN locations l ON r.location_id = l.location_id
        WHERE r.data_type = ?
        GROUP BY r.state, r.district
        ORDER BY r.state, r.district
    """, (data_type,))
    return jsonify({
        'count': len(locations),
        'data_type': data_type,
        'locations': locations
    })

@data_bp.route('/api/water-quality', methods=['GET'])
def get_water_quality():
    data_type = request.args.get('data_type', 'REAL_PUBLIC_SOURCE')
    district = request.args.get('district')
    
    file_name = 'synthetic_demo_dataset.csv' if data_type == 'SYNTHETIC_DEMO' else 'JalRakshak_Integrated_Dataset.csv'
    csv_path = os.path.join(PROCESSED_DIR, file_name)

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if district:
            df = df[df['district'].str.contains(district, case=False, na=False)]
        
        records = df[['record_id', 'state', 'district', 'station_location', 'year', 'season',
                      'ph', 'ec_us_cm', 'tds_mg_l', 'cl_mg_l', 'no3_mg_l', 'so4_mg_l', 'f_mg_l',
                      'total_hardness_mg_l', 'fe_mg_l', 'as_ppb', 'u_ppb', 'water_source']].to_dict(orient='records')
    else:
        records = []

    return jsonify({
        'count': len(records),
        'data_type': data_type,
        'disclaimer': 'Water-quality measurements are environmental indicators and do not by themselves confirm the presence of pathogens.',
        'records': records
    })

@data_bp.route('/api/rainfall', methods=['GET'])
def get_rainfall():
    data_type = request.args.get('data_type', 'REAL_PUBLIC_SOURCE')
    
    file_name = 'synthetic_demo_dataset.csv' if data_type == 'SYNTHETIC_DEMO' else 'JalRakshak_Integrated_Dataset.csv'
    csv_path = os.path.join(PROCESSED_DIR, file_name)

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df_rf = df[['year', 'month', 'season', 'district', 'state', 'rainfall_mm', 'rainfall_anomaly', 'rainfall_source']].dropna(subset=['rainfall_mm'])
        records = df_rf.to_dict(orient='records')
    else:
        records = []

    return jsonify({
        'count': len(records),
        'data_type': data_type,
        'records': records
    })

@data_bp.route('/api/health-data', methods=['GET'])
def get_health_data():
    data_type = request.args.get('data_type', 'REAL_PUBLIC_SOURCE')
    
    file_name = 'synthetic_demo_dataset.csv' if data_type == 'SYNTHETIC_DEMO' else 'JalRakshak_Integrated_Dataset.csv'
    csv_path = os.path.join(PROCESSED_DIR, file_name)

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df_h = df[['year', 'district', 'state', 'health_value', 'health_indicator', 'health_source']].dropna(subset=['health_value'])
        records = df_h.to_dict(orient='records')
    else:
        records = []

    return jsonify({
        'count': len(records),
        'data_type': data_type,
        'records': records
    })
