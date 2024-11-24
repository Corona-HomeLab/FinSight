# FinSight
Personal Finance app that feeds into AI to answer questions based on the info you provide it.

## Features

- Track personal assets and their values
- Monitor liabilities and debts
- Record financial transactions with categories
- Calculate real-time net worth

## Data Structure

The application stores financial data in CSV format with the following files:

- `assets.csv`: Tracks assets with date, name, and value
- `liabilities.csv`: Records debts with date, name, and amount
- `transactions.csv`: Stores transactions with date, category, description, and amount

## Usage Example

The `FinanceTracker` class in `finance_tracker.py` provides methods to manage your financial data:

- **Add Asset**: Use `add_asset(name: str, value: float)` to add a new asset.
- **Add Liability**: Use `add_liability(name: str, amount: float)` to add a new liability.
- **Add Transaction**: Use `add_transaction(category: str, description: str, amount: float)` to record a transaction.
- **Calculate Net Worth**: Use `calculate_net_worth()` to compute the current net worth.

### Example Code

```python
tracker = FinanceTracker()

tracker.add_asset("Savings Account", 5000)
tracker.add_asset("Car", 15000)
tracker.add_liability("Credit Card", 1000)
tracker.add_liability("Student Loan", 20000)
tracker.add_transaction("Food", "Grocery shopping", -150.50)

net_worth = tracker.calculate_net_worth()
print(f"Current Net Worth: ${net_worth:,.2f}")
```

This example demonstrates how to use the `FinanceTracker` class to manage your finances and calculate your net worth.
