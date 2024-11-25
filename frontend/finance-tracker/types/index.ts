export interface FinancialRecord {
    date: string;
    amount: number;
    category: 'Income' | 'Expense';
    description: string;
  }
  
  export interface NetWorthData {
    net_worth: number;
    total_income: number;
    total_expenses: number;
  }