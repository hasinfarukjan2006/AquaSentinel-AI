from flask import Blueprint, jsonify, request
from backend.database import query_db

alert_bp = Blueprint('alert', __name__)

@alert_bp.route('/api/alerts', methods=['GET'])
def get_alerts():
    data_type = request.args.get('data_type', 'SYNTHETIC_DEMO')
    alert_level = request.args.get('level')

    query = "SELECT * FROM alerts WHERE data_type = ?"
    params = [data_type]

    if alert_level:
        query += " AND alert_level = ?"
        params.append(alert_level)

    query += " ORDER BY risk_score DESC"
    alerts = query_db(query, params)

    return jsonify({
        'count': len(alerts),
        'data_type': data_type,
        'alerts': alerts
    })
