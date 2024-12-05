from flask import Blueprint, jsonify, request
from app.models.finance import FinanceTracker
import os

api = Blueprint('api', __name__, url_prefix='/api')
tracker = FinanceTracker()

@api.route('/individuals', methods=['GET'])
def get_individuals():
    try:
        individuals = tracker.get_individuals()
        print(f"Retrieved individuals: {individuals}")
        return jsonify(individuals)
    except Exception as e:
        print(f"Error in get_individuals: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/individuals', methods=['POST'])
def add_individual():
    try:
        data = request.json
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        success = tracker.add_individual(name)
        if success:
            return jsonify({'message': 'Individual added successfully'})
        return jsonify({'error': 'Failed to add individual'}), 500
    except Exception as e:
        print(f"Error in add_individual: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/records', methods=['GET'])
@api.route('/records/<individual>', methods=['GET'])
def get_records(individual=None):
    try:
        print(f"Getting records for individual: {individual}")
        record_type = request.args.get('type')
        if individual:
            records = tracker.view_records(individual, record_type)
        else:
            records = tracker.view_records(record_type)
        print(f"Records found: {records}")
        return jsonify(records)
    except Exception as e:
        print(f"Error in get_records: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/records', methods=['POST'])
@api.route('/records/<individual>', methods=['POST'])
def add_record(individual=None):
    try:
        data = request.json
        print(f"Received data: {data}")
        amount = float(data['amount'])
        category = data['category']
        
        if category == 'Expense':
            amount = -abs(amount)
        else:
            amount = abs(amount)
            
        if individual:
            success = tracker.add_record(individual, amount, category, data['description'])
        else:
            success = tracker.add_record(amount, category, data['description'])
            
        if success:
            return jsonify({'message': 'Record added successfully'})
        return jsonify({'error': 'Failed to add record'}), 500
    except Exception as e:
        print(f"Error in add_record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/net-worth', methods=['GET'])
@api.route('/net-worth/<individual>', methods=['GET'])
def get_net_worth(individual=None):
    try:
        print(f"Calculating net worth for individual: {individual}")
        if individual:
            data = tracker.calculate_net_worth(individual)
        else:
            data = tracker.calculate_net_worth()
        print(f"Net worth data: {data}")
        return jsonify(data)
    except Exception as e:
        print(f"Error in get_net_worth: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/records/<int:index>', methods=['PUT'])
def update_record(index):
    try:
        data = request.json
        amount = float(data['amount'])
        category = data['category']
        description = data['description']
        
        success = tracker.edit_record(index, amount, category, description)
        if success:
            return jsonify({'message': 'Record updated successfully'})
        return jsonify({'error': 'Failed to update record'}), 404
    except Exception as e:
        print(f"Error in update_record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/records/<int:index>', methods=['DELETE'])
def delete_record(index):
    try:
        success = tracker.delete_record(index)
        if success:
            return jsonify({'message': 'Record deleted successfully'})
        return jsonify({'error': 'Failed to delete record'}), 404
    except Exception as e:
        print(f"Error in delete_record: {str(e)}")
        return jsonify({'error': str(e)}), 500