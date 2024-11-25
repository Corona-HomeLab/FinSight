# FinSight
Personal Finance app that feeds into AI to answer questions based on the info you provide it.

## Features

- Record financial transactions with categories
- Track income and expenses
- Calculate real-time net worth
- Edit existing financial records

## Data Structure

The application stores financial data in CSV format with the following file:

- `data.csv`: Stores records with date, amount, category, and description

## Usage Example

The `FinanceTracker` class in `app/models/finance.py` provides methods to manage your financial data:

- **Add Record**: Use `add_record(amount: float, category: str, description: str)` to add an income (positive amount) or expense (negative amount) record.
- **Calculate Net Worth**: Use `calculate_net_worth()` to compute the current net worth.
- **View Records**: Use `view_records(record_type=None)` to view all records, or filter by 'income' or 'expense'.
- **Edit Record**: Use `edit_record(index: int, amount: float, category: str, description: str)` to modify an existing record.

### Example Code

```python
tracker = FinanceTracker()

tracker.add_record(5000, "Income", "Salary")
tracker.add_record(-150.50, "Expense", "Grocery shopping")

net_worth_data = tracker.calculate_net_worth()
print(f"Current Net Worth: ${net_worth_data['net_worth']:,.2f}")
```

This example demonstrates how to use the `FinanceTracker` class to manage your finances, track income and expenses, and calculate your net worth.

## Web Interface

The application also provides a web interface built with Flask. You can perform the following actions through the web interface:

- **Add Record**: Navigate to `/add_record` to add a new financial record.
- **View Records**: Navigate to `/view_records` to see all your financial records.
- **Edit Record**: Edit existing records directly from the records view.
- **Net Worth Report**: Navigate to `/net_worth` to view a summary of your total income, expenses, and net worth.

To run the web application, execute the following command:

```bash
python run.py
```

The application will be available at `http://localhost:5000`.
