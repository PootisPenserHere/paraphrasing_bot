from flask import Blueprint, jsonify

generic_blueprint = Blueprint('generic_blueprint', __name__)


@generic_blueprint.route('/health-check', methods=['GET'])
def health_check():
    return jsonify({"message": "Process running!"})
