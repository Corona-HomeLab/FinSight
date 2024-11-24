import csv
from datetime import datetime
from pathlib import Path

class FinanceTracker:
    def __init__(self):
        self.data_folder = Path("finance_data")
        self.data_folder.mkdir(exist_ok=True)
        
        self.assets_file = self.data_folder / "assets.csv"
        self.liabilities_file = self.data_folder / "liabilities.csv"
        self.transactions_file = self.data_folder / "transactions.csv"
        
        self._initialize_files()
    
    def _initialize_files(self):
        if not self.assets_file.exists():
            with open(self.assets_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'name', 'value'])
        
        if not self.liabilities_file.exists():
            with open(self.liabilities_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'name', 'amount'])
        
        if not self.transactions_file.exists():
            with open(self.transactions_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'category', 'description', 'amount'])

    def add_asset(self, name: str, value: float):
        with open(self.assets_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().date(), name, value])

    def add_liability(self, name: str, amount: float):
        with open(self.liabilities_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().date(), name, amount])

    def add_transaction(self, category: str, description: str, amount: float):
        with open(self.transactions_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().date(), category, description, amount])

    def calculate_net_worth(self):
        total_assets = 0
        total_liabilities = 0

        with open(self.assets_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_assets += float(row['value'])

        with open(self.liabilities_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_liabilities += float(row['amount'])

        return total_assets - total_liabilities

if __name__ == "__main__":
    tracker = FinanceTracker()
    
    tracker.add_asset("Savings Account", 5000)
    tracker.add_asset("Car", 15000)
    tracker.add_liability("Credit Card", 1000)
    tracker.add_liability("Student Loan", 20000)
    tracker.add_transaction("Food", "Grocery shopping", -150.50)
    
    net_worth = tracker.calculate_net_worth()
    print(f"Current Net Worth: ${net_worth:,.2f}")