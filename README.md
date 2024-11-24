# FinSight
Personal Finance app that feeds into AI to answer questions based on the info you provide it.

## Features

- Record financial transactions with categories
- Track income and expenses
- Calculate real-time net worth

## Data Structure

The application stores financial data in CSV format with the following file:

- `data.csv`: Stores records with date, amount, category, and description

## Usage Example

The `FinanceTracker` class in `finance_tracker.py` provides methods to manage your financial data:

- **Add Record**: Use `add_record(amount: float, category: str, description: str)` to add an income (positive amount) or expense (negative amount) record.
- **Calculate Net Worth**: Use `calculate_net_worth()` to compute the current net worth.
- **View Records**: Use `view_records(record_type=None)` to view all records, or filter by 'income' or 'expense'.

### Example Code

```python
tracker = FinanceTracker()

tracker.add_record(5000, "Income", "Salary")
tracker.add_record(-150.50, "Expense", "Grocery shopping")

net_worth_data = tracker.calculate_net_worth()
print(f"Current Net Worth: ${net_worth_data['net_worth']:,.2f}")
```

This example demonstrates how to use the `FinanceTracker` class to manage your finances, track income and expenses, and calculate your net worth.
