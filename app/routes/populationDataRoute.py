from flask import Blueprint, request, jsonify
from app.utils.db_utils import get_db_connection
from app.config.database import DB_CONFIG
from app.models.populationDataModel import get_population_data

population_bp = Blueprint('population', __name__)


@population_bp.route('/api/populationData', methods=['POST'])
def get_population_data_endpoint():
    data = request.get_json()

    if not data or 'country_name' not in data:
        return jsonify({'error': 'Country name is required'}), 400

    country_name = data['country_name'].strip()

    conn = get_db_connection(DB_CONFIG)
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        result = get_population_data(conn, country_name)
        if result:
            return jsonify({'data': result}), 200
        else:
            return jsonify({'message': f'No data found for country: {country_name}'}), 404
    finally:
        conn.close()
