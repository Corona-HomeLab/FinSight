import csv
from datetime import datetime
from pathlib import Path
import sys

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

    def view_assets(self):
        return self._read_csv(self.assets_file)

    def view_liabilities(self):
        return self._read_csv(self.liabilities_file)

    def view_transactions(self):
        return self._read_csv(self.transactions_file)

    def _read_csv(self, file_path):
        with open(file_path, 'r') as f:
            return list(csv.DictReader(f))

    def update_asset(self, name: str, new_value: float):
        self._update_record(self.assets_file, 'name', name, 'value', new_value)

    def update_liability(self, name: str, new_amount: float):
        self._update_record(self.liabilities_file, 'name', name, 'amount', new_amount)

    def _update_record(self, file_path, search_field, search_value, update_field, new_value):
        rows = self._read_csv(file_path)
        updated = False
        
        for row in rows:
            if row[search_field] == search_value:
                row[update_field] = new_value
                row['date'] = datetime.now().date()
                updated = True
                break

        if updated:
            headers = rows[0].keys()
            with open(file_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
        else:
            print(f"No record found with {search_field}: {search_value}")

    def delete_asset(self, name: str):
        self._delete_record(self.assets_file, 'name', name)

    def delete_liability(self, name: str):
        self._delete_record(self.liabilities_file, 'name', name)

    def _delete_record(self, file_path, search_field, search_value):
        rows = self._read_csv(file_path)
        original_length = len(rows)
        rows = [row for row in rows if row[search_field] != search_value]
        
        if len(rows) < original_length:
            headers = rows[0].keys() if rows else ['date', 'name', 'value']
            with open(file_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
        else:
            print(f"No record found with {search_field}: {search_value}")

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
                    print(f"{liability['date']} - {liability['name']}: ${float(liability['amount']):,.2f}")
            elif sub_choice == "3":
                transactions = tracker.view_transactions()
                print("\nTransactions:")
                for transaction in transactions:
                    print(f"{transaction['date']} - {transaction['category']} - {transaction['description']}: ${float(transaction['amount']):,.2f}")
        
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