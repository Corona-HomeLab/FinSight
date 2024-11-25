from flask import Blueprint, jsonify, request
from app.models.finance import FinanceTracker
import os

api = Blueprint('api', __name__, url_prefix='/api')
tracker = FinanceTracker()

@api.route('/records', methods=['GET'])
def get_records():
    try:
        print(f"Data file path: {tracker.data_file}")
        print(f"Data file exists: {os.path.exists(tracker.data_file)}")
        record_type = request.args.get('type')
        records = tracker.view_records(record_type)
        print(f"Records found: {records}")
        return jsonify(records)
    except Exception as e:
        print(f"Error in get_records: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/records', methods=['POST'])
def add_record():
    try:
        data = request.json
        print(f"Received data: {data}")
        amount = float(data['amount'])
        category = data['category']
        
        # Make amount negative if it's an expense
        if category == 'Expense':
            amount = -abs(amount)
        else:
            amount = abs(amount)
            
        success = tracker.add_record(amount, category, data['description'])
        if success:
            return jsonify({'message': 'Record added successfully'})
        return jsonify({'error': 'Failed to add record'}), 500
    except Exception as e:
        print(f"Error in add_record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/net-worth', methods=['GET'])
def get_net_worth():
    try:
        print("Calculating net worth...")
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