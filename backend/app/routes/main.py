from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.finance import FinanceTracker

main = Blueprint('main', __name__)
tracker = FinanceTracker()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        record_type = request.form['type']
        description = request.form['description']
        amount = float(request.form['amount'])
        
        final_amount = amount if record_type == 'Income' else -amount
        tracker.add_record(final_amount, record_type, description)
        flash('Record added successfully!')
        return redirect(url_for('main.index'))
    
    return render_template('add_record.html')

@main.route('/view_records')
def view_records():
    record_type = request.args.get('type')
    records = tracker.view_records(record_type)
    return render_template('view_records.html', records=records)

@main.route('/net_worth')
def net_worth():
    data = tracker.calculate_net_worth()
    return render_template('net_worth.html', data=data)

@main.route('/edit_record/<int:index>', methods=['GET', 'POST'])
def edit_record(index):
    if request.method == 'POST':
        record_type = request.form['type']
        description = request.form['description']
        amount = float(request.form['amount'])
        
        final_amount = amount if record_type == 'Income' else -amount
        if tracker.edit_record(index, final_amount, record_type, description):
            flash('Record updated successfully!')
        else:
            flash('Error updating record!')
        return redirect(url_for('main.view_records'))
    
    records = tracker.view_records()
    if 0 <= index < len(records):
        record = records[index]
        return render_template('edit_record.html', record=record, index=index)
    return redirect(url_for('main.view_records'))