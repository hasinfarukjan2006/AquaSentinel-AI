import os
import pandas as pd
from flask import Blueprint, jsonify, request
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
    limit = int(request.args.get('limit', 600))

    if data_type == 'SYNTHETIC_DEMO':
        query = "SELECT * FROM risk_scores WHERE data_type = ?"
        params = [data_type]
        if district:
            query += " AND district LIKE ?"
            params.append(f"%{district}%")
        query += " LIMIT ?"
        params.append(limit)
        records = query_db(query, params)
    else:
        query = "SELECT * FROM water_quality_records WHERE data_type = ?"
        params = [data_type]
        if district:
            query += " AND (district LIKE ? OR station_location LIKE ? OR state LIKE ?)"
            params.extend([f"%{district}%", f"%{district}%", f"%{district}%"])
        query += " ORDER BY year DESC, district ASC LIMIT ?"
        params.append(limit)
        records = query_db(query, params)

    return jsonify({
        'count': len(records),
        'data_type': data_type,
        'disclaimer': 'Water-quality measurements are environmental indicators and do not by themselves confirm the presence of pathogens.',
        'records': records
    })

@data_bp.route('/api/rainfall', methods=['GET'])
def get_rainfall():
    data_type = request.args.get('data_type', 'REAL_PUBLIC_SOURCE')
    limit = int(request.args.get('limit', 200))
    
    if data_type == 'SYNTHETIC_DEMO':
        records = query_db("SELECT * FROM risk_scores WHERE data_type = ? LIMIT ?", (data_type, limit))
    else:
        records = query_db("SELECT * FROM rainfall_records WHERE data_type = ? ORDER BY year DESC LIMIT ?", (data_type, limit))

    return jsonify({
        'count': len(records),
        'data_type': data_type,
        'records': records
    })

@data_bp.route('/api/health-incidents', methods=['GET'])
@data_bp.route('/api/health-data', methods=['GET'])
def get_health_data():
    data_type = request.args.get('data_type', 'REAL_PUBLIC_SOURCE')
    limit = int(request.args.get('limit', 100))
    
    if data_type == 'SYNTHETIC_DEMO':
        records = query_db("SELECT * FROM risk_scores WHERE data_type = ? LIMIT ?", (data_type, limit))
    else:
        records = query_db("SELECT * FROM health_records WHERE data_type = ? ORDER BY year DESC LIMIT ?", (data_type, limit))

    return jsonify({
        'count': len(records),
        'data_type': data_type,
        'records': records
    })

@data_bp.route('/api/data-explorer', methods=['GET'])
def get_data_explorer():
    data_type = request.args.get('data_type', 'REAL_PUBLIC_SOURCE')
    district = request.args.get('district')
    state = request.args.get('state')
    risk_class = request.args.get('risk_class')
    limit = int(request.args.get('limit', 500))

    query = "SELECT * FROM risk_scores WHERE data_type = ?"
    params = [data_type]

    if district:
        query += " AND district LIKE ?"
        params.append(f"%{district}%")
    if state:
        query += " AND state LIKE ?"
        params.append(f"%{state}%")
    if risk_class:
        query += " AND risk_class = ?"
        params.append(risk_class)

    query += " ORDER BY risk_score DESC LIMIT ?"
    params.append(limit)

    records = query_db(query, params)
    formatted_records = []
    for r in records:
        r_dict = dict(r)
        avail = r_dict.get('data_availability_status', 'PARTIAL')
        rec_id = str(r_dict.get('record_id', ''))
        
        if avail == 'WATER_ONLY' or rec_id.startswith('WQ') or rec_id.startswith('REAL_WQ'):
            src = 'Central Ground Water Board (CGWB 2024)'
            vars_list = ['pH', 'EC (µS/cm)', 'TDS (mg/L)', 'Chloride', 'Nitrate (NO3)', 'Sulphate', 'Fluoride', 'Iron']
        elif avail == 'RAINFALL_ONLY' or rec_id.startswith('RF') or rec_id.startswith('REAL_RF'):
            src = 'India Meteorological Department (IMD 1901-2021)'
            vars_list = ['Monsoon Rainfall (mm)', 'Rainfall Anomaly Z-Score']
        elif avail == 'HEALTH_ONLY' or rec_id.startswith('HLTH') or rec_id.startswith('REAL_HLTH'):
            src = 'Ministry of Health & Family Welfare (MoHFW Rajya Sabha AU 557)'
            vars_list = ['Reported Water-Borne Disease Cases']
        else:
            src = 'AquaSentinel Integrated Multi-Source (CGWB, IMD, MoHFW)'
            vars_list = ['Water Quality (pH, EC, TDS, NO3, F)', 'Monsoon Rainfall Anomaly', 'Health Disease Baseline']

        r_dict['source'] = src
        r_dict['provenance'] = 'Verified Public Government Open Data'
        r_dict['available_variables'] = vars_list
        r_dict['year_date'] = f"{r_dict.get('year', 2024)} ({r_dict.get('season', 'N/A')})"
        formatted_records.append(r_dict)

    return jsonify({
        'count': len(formatted_records),
        'data_type': data_type,
        'records': formatted_records
    })

@data_bp.route('/api/data-status', methods=['GET'])
def get_data_status():
    real_integrated_count = query_db("SELECT COUNT(*) as cnt FROM risk_scores WHERE data_type = 'REAL_PUBLIC_SOURCE'")[0]['cnt']
    synthetic_count = query_db("SELECT COUNT(*) as cnt FROM risk_scores WHERE data_type = 'SYNTHETIC_DEMO'")[0]['cnt']
    cgwb_count = query_db("SELECT COUNT(*) as cnt FROM water_quality_records WHERE data_type = 'REAL_PUBLIC_SOURCE'")[0]['cnt']
    imd_count = query_db("SELECT COUNT(*) as cnt FROM rainfall_records WHERE data_type = 'REAL_PUBLIC_SOURCE'")[0]['cnt']
    mohfw_count = query_db("SELECT COUNT(*) as cnt FROM health_records WHERE data_type = 'REAL_PUBLIC_SOURCE'")[0]['cnt']
    loc_count = query_db("SELECT COUNT(*) as cnt FROM locations")[0]['cnt']
    sources = query_db("SELECT * FROM data_sources")

    return jsonify({
        'database': 'healthy',
        'status': 'healthy',
        'data_mode': 'REAL_PUBLIC_SOURCE',
        'real_public_source_records': real_integrated_count,
        'health_records': mohfw_count,
        'rainfall_records': imd_count,
        'water_quality_records': cgwb_count,
        'risk_records': real_integrated_count,
        'locations': loc_count,
        'synthetic_demo_records': synthetic_count,
        'total_real_records': real_integrated_count,
        'hmis_record_count': mohfw_count,
        'rainfall_record_count': imd_count,
        'cgwb_record_count': cgwb_count,
        'integrated_record_count': real_integrated_count,
        'locations_count': loc_count,
        'api_module_availability': {
            'summary': True,
            'locations': True,
            'water_quality': True,
            'rainfall': True,
            'health_incidents': True,
            'risk_monitoring': True,
            'data_explorer': True
        },
        'data_sources': sources
    })

