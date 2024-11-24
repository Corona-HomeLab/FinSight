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
                writer.writerow(['date', 'type', 'name', 'value', 'category', 'description'])

    def add_asset(self, name: str, value: float):
        with open(self.data_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().date(), 'asset', name, value, '', ''])

    def add_liability(self, name: str, amount: float):
        with open(self.data_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().date(), 'liability', name, amount, '', ''])

    def add_transaction(self, category: str, description: str, amount: float):
        with open(self.data_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().date(), 'transaction', '', amount, category, description])

    def calculate_net_worth(self):
        total_assets = 0
        total_liabilities = 0

        with open(self.data_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['type'] == 'asset':
                    total_assets += float(row['value'])
                elif row['type'] == 'liability':
                    total_liabilities += float(row['value'])

        return total_assets - total_liabilities

    def view_assets(self):
        return self._read_filtered_csv('asset')

    def view_liabilities(self):
        return self._read_filtered_csv('liability')

    def view_transactions(self):
        return self._read_filtered_csv('transaction')

    def _read_filtered_csv(self, record_type):
        with open(self.data_file, 'r') as f:
            return [row for row in csv.DictReader(f) if row['type'] == record_type]

    def update_asset(self, name: str, new_value: float):
        self._update_record('asset', name, new_value)

    def update_liability(self, name: str, new_amount: float):
        self._update_record('liability', name, new_amount)

    def _update_record(self, record_type, name, new_value):
        rows = self._read_csv(self.data_file)
        updated = False
        
        for row in rows:
            if row['type'] == record_type and row['name'] == name:
                row['value'] = new_value
                row['date'] = datetime.now().date()
                updated = True
                break

        if updated:
            headers = rows[0].keys()
            with open(self.data_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
        else:
            print(f"No {record_type} found with name: {name}")

    def delete_asset(self, name: str):
        self._delete_record('asset', name)

    def delete_liability(self, name: str):
        self._delete_record('liability', name)

    def _delete_record(self, record_type, name):
        rows = self._read_csv(self.data_file)
        original_length = len(rows)
        rows = [row for row in rows if not (row['type'] == record_type and row['name'] == name)]
        
        if len(rows) < original_length:
            headers = rows[0].keys() if rows else ['date', 'type', 'name', 'value', 'category', 'description']
            with open(self.data_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
        else:
            print(f"No {record_type} found with name: {name}")

    def _read_csv(self, file_path):
        with open(file_path, 'r') as f:
            return list(csv.DictReader(f))

def main():
    tracker = FinanceTracker()
    
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Record")
        print("2. View Records")
        print("3. Update Record")
        print("4. Delete Record")
        print("5. Calculate Net Worth")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            print("\nAdd Record:")
            print("1. Asset")
            print("2. Liability")
            print("3. Transaction")
            sub_choice = input("Enter choice (1-3): ")
            
            if sub_choice == "1":
                name = input("Enter asset name: ")
                value = float(input("Enter asset value: "))
                tracker.add_asset(name, value)
            elif sub_choice == "2":
                name = input("Enter liability name: ")
                amount = float(input("Enter liability amount: "))
                tracker.add_liability(name, amount)
            elif sub_choice == "3":
                category = input("Enter transaction category: ")
                description = input("Enter description: ")
                amount = float(input("Enter amount (negative for expenses): "))
                tracker.add_transaction(category, description, amount)
        
        elif choice == "2":
            print("\nView Records:")
            print("1. Assets")
            print("2. Liabilities")
            print("3. Transactions")
            sub_choice = input("Enter choice (1-3): ")
            
            if sub_choice == "1":
                assets = tracker.view_assets()
                print("\nAssets:")
                for asset in assets:
                    print(f"{asset['date']} - {asset['name']}: ${float(asset['value']):,.2f}")
            elif sub_choice == "2":
                liabilities = tracker.view_liabilities()
                print("\nLiabilities:")
                for liability in liabilities:
                    print(f"{liability['date']} - {liability['name']}: ${float(liability['value']):,.2f}")
            elif sub_choice == "3":
                transactions = tracker.view_transactions()
                print("\nTransactions:")
                for transaction in transactions:
                    print(f"{transaction['date']} - {transaction['category']} - {transaction['description']}: ${float(transaction['value']):,.2f}")
        
        elif choice == "3":
            print("\nUpdate Record:")
            print("1. Asset")
            print("2. Liability")
            sub_choice = input("Enter choice (1-2): ")
            
            if sub_choice == "1":
                name = input("Enter asset name to update: ")
                new_value = float(input("Enter new value: "))
                tracker.update_asset(name, new_value)
            elif sub_choice == "2":
                name = input("Enter liability name to update: ")
                new_amount = float(input("Enter new amount: "))
                tracker.update_liability(name, new_amount)
        
        elif choice == "4":
            print("\nDelete Record:")
            print("1. Asset")
            print("2. Liability")
            sub_choice = input("Enter choice (1-2): ")
            
            if sub_choice == "1":
                name = input("Enter asset name to delete: ")
                tracker.delete_asset(name)
            elif sub_choice == "2":
                name = input("Enter liability name to delete: ")
                tracker.delete_liability(name)
        
        elif choice == "5":
            net_worth = tracker.calculate_net_worth()
            print(f"\nCurrent Net Worth: ${net_worth:,.2f}")
        
        elif choice == "6":
            print("\nThank you for using Personal Finance Tracker!")
            sys.exit(0)
        
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()