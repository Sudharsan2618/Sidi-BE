from flask import Blueprint, jsonify
from app.utils.db_utils import get_db_connection
from app.config.database import DB_CONFIG
from app.models.populationMasterModel import get_population_data_for_current_year


population_percentage_bp = Blueprint('population_percentage', __name__)

@population_percentage_bp.route('/api/populationPercentage', methods=['GET'])
def get_population_data_for_current_year_endpoint():
    conn = get_db_connection(DB_CONFIG)
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        result = get_population_data_for_current_year(conn)
        if result:
            return jsonify({'data': result}), 200
        else:
            return jsonify({'message': 'No data found for the current year'}), 404
    finally:
        conn.close()
