import csv
from datetime import datetime
from pathlib import Path
import sys

class FinanceTracker:
    def __init__(self):
        self.data_folder = Path("finance_data")
        self.data_folder.mkdir(exist_ok=True)
        self.data_file = self.data_folder / "data.csv"
        self._initialize_file()
    
    def _initialize_file(self):
        if not self.data_file.exists():
            with open(self.data_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'amount', 'category', 'description'])

    def add_record(self, amount: float, category: str, description: str):
        """Add an income (positive amount) or expense (negative amount) record"""
        with open(self.data_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().date(), amount, category, description])

    def calculate_net_worth(self):
        """Calculate net worth based on all historical income and expenses"""
        income_total = 0
        expenses_total = 0
        
        with open(self.data_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                amount = float(row['amount'])
                if amount > 0:
                    income_total += amount
                else:
                    expenses_total += abs(amount)
        
        return {
            'net_worth': income_total - expenses_total,
            'total_income': income_total,
            'total_expenses': expenses_total
        }

    def view_records(self, record_type=None):
        """View all records, or filter by 'income' or 'expense'"""
        with open(self.data_file, 'r') as f:
            records = list(csv.DictReader(f))
            # Convert amount to float in each record
            for record in records:
                record['amount'] = float(record['amount'])
            
            if record_type == 'income':
                return [r for r in records if r['amount'] > 0]
            elif record_type == 'expense':
                return [r for r in records if r['amount'] < 0]
            return records

    def edit_record(self, index: int, amount: float, category: str, description: str):
        """Edit a record at the specified index"""
        records = []
        with open(self.data_file, 'r') as f:
            reader = csv.DictReader(f)
            records = list(reader)
        
        if 0 <= index < len(records):
            records[index]['amount'] = amount
            records[index]['category'] = category
            records[index]['description'] = description
            
            with open(self.data_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'amount', 'category', 'description'])
                writer.writeheader()
                writer.writerows(records)
            return True
        return False

def main():
    tracker = FinanceTracker()
    
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Record")
        print("2. View Records")
        print("3. View Net Worth Report")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            print("\nAdd Record:")
            print("1. Income")
            print("2. Expense")
            sub_choice = input("Enter choice (1-2): ")
            
            category = "Income" if sub_choice == "1" else "Expense"
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            
            if sub_choice == "2":  # Expense
                amount = -amount  # Make amount negative for expenses
            
            tracker.add_record(amount, category, description)
            print("Record added successfully!")
            
        elif choice == "2":
            print("\nView Records:")
            print("1. All Records")
            print("2. Income Only")
            print("3. Expenses Only")
            sub_choice = input("Enter choice (1-3): ")
            
            record_type = None
            if sub_choice == "2":
                record_type = "income"
            elif sub_choice == "3":
                record_type = "expense"
                
            records = tracker.view_records(record_type)
            print("\nRecords:")
            for record in records:
                print(f"{record['date']} - {record['category']} - {record['description']}: ${float(record['amount']):,.2f}")
        
        elif choice == "3":
            net_worth_data = tracker.calculate_net_worth()
            print("\n=== Net Worth Report ===")
            print(f"Total Income: ${net_worth_data['total_income']:,.2f}")
            print(f"Total Expenses: ${net_worth_data['total_expenses']:,.2f}")
            print(f"Net Worth: ${net_worth_data['net_worth']:,.2f}")
        
        elif choice == "4":
            print("\nThank you for using Personal Finance Tracker!")
            sys.exit(0)
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()