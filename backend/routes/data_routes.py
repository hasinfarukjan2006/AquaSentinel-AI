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
    return jsonify({
        'count': len(records),
        'data_type': data_type,
        'records': records
    })

@data_bp.route('/api/data-status', methods=['GET'])
def get_data_status():
    real_integrated_count = query_db("SELECT COUNT(*) as cnt FROM risk_scores WHERE data_type = 'REAL_PUBLIC_SOURCE'")[0]['cnt']
    cgwb_count = query_db("SELECT COUNT(*) as cnt FROM water_quality_records WHERE data_type = 'REAL_PUBLIC_SOURCE'")[0]['cnt']
    imd_count = query_db("SELECT COUNT(*) as cnt FROM rainfall_records WHERE data_type = 'REAL_PUBLIC_SOURCE'")[0]['cnt']
    mohfw_count = query_db("SELECT COUNT(*) as cnt FROM health_records WHERE data_type = 'REAL_PUBLIC_SOURCE'")[0]['cnt']
    loc_count = query_db("SELECT COUNT(*) as cnt FROM locations")[0]['cnt']
    sources = query_db("SELECT * FROM data_sources")

    return jsonify({
        'status': 'healthy',
        'data_mode': 'REAL_PUBLIC_SOURCE',
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
