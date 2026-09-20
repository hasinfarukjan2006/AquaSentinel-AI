import os
import json
import pandas as pd
from flask import Blueprint, jsonify, request
from backend.config import Config, REPORTS_DIR, ML_REPORT_DIR
from backend.database import query_db

health_bp = Blueprint('health', __name__)

@health_bp.route('/api/health', methods=['GET'])
def api_health():
    db_status = "healthy"
    db_count = 0
    try:
        row = query_db("SELECT COUNT(*) as cnt FROM risk_scores", one=True)
        db_count = row['cnt'] if row else 0
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return jsonify({
        'status': 'healthy' if db_status == "healthy" else 'degraded',
        'service': 'AquaSentinel REST API',
        'version': '1.0.0',
        'database': db_status,
        'total_indexed_records': db_count,
        'environment': os.environ.get('FLASK_ENV', 'production'),
        'tagline': 'From Water Risk to Early Action.',
        'disclaimer': 'AquaSentinel is a prototype decision-support system for community-level early warning. Risk scores are not medical diagnoses and do not confirm disease outbreaks.'
    })

@health_bp.route('/api/summary', methods=['GET'])
def api_summary():
    data_type = request.args.get('data_type', 'REAL_PUBLIC_SOURCE') # Default to REAL production records
    
    total_locations = query_db("SELECT COUNT(DISTINCT district) as cnt FROM risk_scores WHERE data_type = ?", (data_type,), one=True)['cnt']
    total_records = query_db("SELECT COUNT(*) as cnt FROM risk_scores WHERE data_type = ?", (data_type,), one=True)['cnt']
    
    risk_dist = query_db("""
        SELECT risk_class, COUNT(*) as count 
        FROM risk_scores 
        WHERE data_type = ? 
        GROUP BY risk_class
    """, (data_type,))

    high_risk_locs = query_db("""
        SELECT DISTINCT district, state, risk_score, risk_class, data_availability_status
        FROM risk_scores 
        WHERE data_type = ?
        ORDER BY risk_score DESC
        LIMIT 10
    """, (data_type,))

    abnormal_count = query_db("""
        SELECT COUNT(*) as cnt FROM risk_scores 
        WHERE data_type = ? AND abnormal_pattern_flag = 1
    """, (data_type,), one=True)['cnt']

    return jsonify({
        'monitored_locations': total_locations,
        'total_records': total_records,
        'risk_distribution': {r['risk_class']: r['count'] for r in risk_dist},
        'high_risk_locations': high_risk_locs,
        'abnormal_patterns_detected': abnormal_count,
        'pipeline_status': 'Operational',
        'ml_status': 'Available',
        'data_type_active': data_type
    })

@health_bp.route('/api/data-quality', methods=['GET'])
def api_data_quality():
    json_path = os.path.join(REPORTS_DIR, 'data_profile.json')
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            profile_data = json.load(f)
    else:
        profile_data = {}

    quality_summary = query_db("""
        SELECT 
            COUNT(*) as total_records,
            SUM(CASE WHEN data_availability_status = 'COMPLETE' THEN 1 ELSE 0 END) as complete_records,
            SUM(CASE WHEN data_availability_status = 'PARTIAL' THEN 1 ELSE 0 END) as partial_records,
            SUM(CASE WHEN data_availability_status = 'WATER_ONLY' THEN 1 ELSE 0 END) as water_only,
            SUM(CASE WHEN data_availability_status = 'RAINFALL_ONLY' THEN 1 ELSE 0 END) as rainfall_only,
            SUM(CASE WHEN data_availability_status = 'HEALTH_ONLY' THEN 1 ELSE 0 END) as health_only
        FROM risk_scores
    """, one=True)

    return jsonify({
        'profile': profile_data,
        'completeness_summary': quality_summary
    })

@health_bp.route('/api/model/status', methods=['GET'])
def api_model_status():
    eval_path = os.path.join(ML_REPORT_DIR, 'model_evaluation.json')
    if os.path.exists(eval_path):
        with open(eval_path, 'r') as f:
            eval_data = json.load(f)
    else:
        eval_data = {}

    return jsonify({
        'model_name': 'Random Forest Prototype Classifier & Isolation Forest Anomaly Detector',
        'model_status': 'Prototype Trained',
        'features_used': ['ph', 'ec_us_cm', 'tds_mg_l', 'cl_mg_l', 'no3_mg_l', 'so4_mg_l', 'f_mg_l', 'total_hardness_mg_l', 'fe_mg_l', 'rainfall_mm', 'health_value'],
        'evaluation': eval_data,
        'disclaimer': 'Prototype risk model — requires validation and calibration using appropriate historical public-health data before operational deployment.'
    })
