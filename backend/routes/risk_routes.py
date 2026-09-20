from flask import Blueprint, jsonify, request
from backend.database import query_db
from ml.predict import RiskPredictor

risk_bp = Blueprint('risk', __name__)
predictor = RiskPredictor()

@risk_bp.route('/api/risk', methods=['GET'])
def get_risk_records():
    data_type = request.args.get('data_type', 'REAL_PUBLIC_SOURCE')
    district = request.args.get('district')
    state = request.args.get('state')
    risk_class = request.args.get('risk_class')
    limit = int(request.args.get('limit', 100))

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

@risk_bp.route('/api/risk/<location>', methods=['GET'])
def get_location_risk(location):
    data_type = request.args.get('data_type', 'REAL_PUBLIC_SOURCE')
    
    records = query_db("""
        SELECT * FROM risk_scores 
        WHERE (district LIKE ? OR state LIKE ?) AND data_type = ?
        ORDER BY risk_score DESC
    """, (f"%{location}%", f"%{location}%", data_type))

    if not records:
        return jsonify({
            'found': False,
            'message': f"No records found for location '{location}' under data_type '{data_type}'."
        }), 404

    latest = records[0]

    # Verification recommendation wording generator
    score = latest['risk_score']
    if score >= 71.0:
        recommendation = "Elevated risk pattern detected — local health and water sample verification recommended immediately."
    elif score >= 51.0:
        recommendation = "Moderate-to-high environmental risk signal — verify local water treatment and reported symptoms."
    else:
        recommendation = "Routine monitoring — indicators currently within acceptable prototype baseline thresholds."

    return jsonify({
        'found': True,
        'location': latest['district'],
        'state': latest['state'],
        'latest_record': latest,
        'historical_trend': records[:15],
        'recommended_action': recommendation,
        'disclaimer': 'Risk scores are decision-support signals and do NOT confirm a disease outbreak.'
    })

@risk_bp.route('/api/risk/predict', methods=['POST'])
def predict_risk():
    data = request.json or {}
    prediction = predictor.predict_record(data)
    return jsonify(prediction)
