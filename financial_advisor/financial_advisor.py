# Basic Virtual Financial Advisor
# A simplified command-line application for financial management

import os
import json
import datetime
import hashlib
from tabulate import tabulate

class FinancialAdvisor:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.data_file = "financial_data.json"
        self.load_data()

    def load_data(self):
        """Load user data from JSON file if it exists"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    self.users = json.load(file)
            except:
                self.users = {}
        else:
            print("No existing data found. Starting fresh.")

    def save_data(self):
        """Save user data to JSON file"""
        with open(self.data_file, 'w') as file:
            json.dump(self.users, file, indent=4)
        print("Data saved successfully.")

    def register_user(self, username, password, initial_balance=0):
        """Register a new user"""
        if username in self.users:
            print("Username already exists. Please choose another.")
            return False

        # Hash the password for security
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Initialize user data structure
        self.users[username] = {
            "password": hashed_password,
            "balance": initial_balance,
            "expenses": [],
            "income": [],
            "budget": {}
        }
        
        self.save_data()
        print(f"User {username} registered successfully!")
        return True

    def login(self, username, password):
        """Login a user"""
        if username not in self.users:
            print("Username not found.")
            return False
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if self.users[username]["password"] != hashed_password:
            print("Incorrect password.")
            return False
        
        self.current_user = username
        print(f"Welcome back, {username}!")
        return True

    def logout(self):
        """Logout the current user"""
        if self.current_user:
            print(f"Goodbye, {self.current_user}!")
            self.current_user = None
            return True
        return False

    def add_expense(self, amount, category, description=""):
        """Add an expense for the current user"""
        if not self.current_user:
            print("Please login first.")
            return False
        
        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.users[self.current_user]["expenses"].append(expense)
        self.users[self.current_user]["balance"] -= amount
        self.save_data()
        print(f"Expense of ${amount:.2f} added to {category}.")
        return True

    def add_income(self, amount, source, description=""):
        """Add income for the current user"""
        if not self.current_user:
            print("Please login first.")
            return False
        
        income = {
            "amount": amount,
            "source": source,
            "description": description,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.users[self.current_user]["income"].append(income)
        self.users[self.current_user]["balance"] += amount
        self.save_data()
        print(f"Income of ${amount:.2f} added from {source}.")
        return True

    def view_balance(self):
        """View the current balance"""
        if not self.current_user:
            print("Please login first.")
            return None
        
        balance = self.users[self.current_user]["balance"]
        print(f"Current balance: ${balance:.2f}")
        return balance

    def view_expenses(self, limit=10):
        """View recent expenses"""
        if not self.current_user:
            print("Please login first.")
            return False
        
        expenses = self.users[self.current_user]["expenses"]
        if not expenses:
            print("No expenses recorded yet.")
            return True
        
        # Sort expenses by date (most recent first)
        sorted_expenses = sorted(expenses, key=lambda x: x["date"], reverse=True)
        
        # Limit the number of expenses shown
        limited_expenses = sorted_expenses[:limit]
        
        # Convert to a format suitable for tabulate
        table_data = []
        for expense in limited_expenses:
            table_data.append([
                expense["date"],
                expense["category"],
                f"${expense['amount']:.2f}",
                expense["description"]
            ])
        
        headers = ["Date", "Category", "Amount", "Description"]
        print("\nRecent Expenses:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Calculate total expenses
        total = sum(expense["amount"] for expense in expenses)
        print(f"Total expenses: ${total:.2f}")
        
        return True

    def view_income(self, limit=10):
        """View recent income"""
        if not self.current_user:
            print("Please login first.")
            return False
        
        income_list = self.users[self.current_user]["income"]
        if not income_list:
            print("No income recorded yet.")
            return True
        
        # Sort income by date (most recent first)
        sorted_income = sorted(income_list, key=lambda x: x["date"], reverse=True)
        
        # Limit the number of income entries shown
        limited_income = sorted_income[:limit]
        
        # Convert to a format suitable for tabulate
        table_data = []
        for income in limited_income:
            table_data.append([
                income["date"],
                income["source"],
                f"${income['amount']:.2f}",
                income["description"]
            ])
        
        headers = ["Date", "Source", "Amount", "Description"]
        print("\nRecent Income:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Calculate total income
        total = sum(income["amount"] for income in income_list)
        print(f"Total income: ${total:.2f}")
        
        return True

    def set_budget(self, category, amount):
        """Set a monthly budget for a specific category"""
        if not self.current_user:
            print("Please login first.")
            return False
        
        if "budget" not in self.users[self.current_user]:
            self.users[self.current_user]["budget"] = {}
        
        self.users[self.current_user]["budget"][category] = amount
        self.save_data()
        print(f"Budget for {category} set to ${amount:.2f} per month.")
        return True

    def view_budget(self):
        """View current budget and spending against it"""
        if not self.current_user:
            print("Please login first.")
            return False
        
        if "budget" not in self.users[self.current_user] or not self.users[self.current_user]["budget"]:
            print("No budget has been set yet.")
            return True
        
        budget = self.users[self.current_user]["budget"]
        expenses = self.users[self.current_user]["expenses"]
        
        # Get current month's expenses
        current_month = datetime.datetime.now().strftime("%Y-%m")
        current_month_expenses = [
            expense for expense in expenses
            if expense["date"].startswith(current_month)
        ]
        
        # Group current month's expenses by category
        monthly_spending = {}
        for expense in current_month_expenses:
            category = expense["category"]
            amount = expense["amount"]
            if category in monthly_spending:
                monthly_spending[category] += amount
            else:
                monthly_spending[category] = amount
        
        # Display budget vs. actual spending
        table_data = []
        for category, budget_amount in budget.items():
            spent = monthly_spending.get(category, 0)
            remaining = budget_amount - spent
            percentage = (spent / budget_amount) * 100 if budget_amount > 0 else 0
            status = "Over Budget" if remaining < 0 else "On Track"
            
            table_data.append([
                category,
                f"${budget_amount:.2f}",
                f"${spent:.2f}",
                f"${remaining:.2f}",
                f"{percentage:.1f}%",
                status
            ])
        
        headers = ["Category", "Budget", "Spent", "Remaining", "Used", "Status"]
        print("\nMonthly Budget Status:")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        return True


class FinancialAdvisorCLI:
    def __init__(self):
        self.advisor = FinancialAdvisor()
        self.running = True

    def run(self):
        """Main application loop"""
        print("Welcome to the Virtual Financial Advisor!")
        print("Type 'help' to see available commands.")
        
        while self.running:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "register":
                username = input("Enter username: ")
                password = input("Enter password: ")
                initial_balance = float(input("Enter initial balance: $"))
                self.advisor.register_user(username, password, initial_balance)
            
            elif command == "login":
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.advisor.login(username, password)
            
            elif command == "logout":
                self.advisor.logout()
            
            elif command == "add_expense":
                if not self.advisor.current_user:
                    print("Please login first.")
                    continue
                try:
                    amount = float(input("Enter amount: $"))
                    category = input("Enter category: ")
                    description = input("Enter description (optional): ")
                    self.advisor.add_expense(amount, category, description)
                except ValueError:
                    print("Invalid amount. Please enter a number.")
            
            elif command == "add_income":
                if not self.advisor.current_user:
                    print("Please login first.")
                    continue
                try:
                    amount = float(input("Enter amount: $"))
                    source = input("Enter source: ")
                    description = input("Enter description (optional): ")
                    self.advisor.add_income(amount, source, description)
                except ValueError:
                    print("Invalid amount. Please enter a number.")
            
            elif command == "view_balance":
                self.advisor.view_balance()
            
            elif command == "view_expenses":
                self.advisor.view_expenses()
            
            elif command == "view_income":
                self.advisor.view_income()
            
            elif command == "set_budget":
                if not self.advisor.current_user:
                    print("Please login first.")
                    continue
                try:
                    category = input("Enter expense category: ")
                    amount = float(input("Enter monthly budget amount: $"))
                    self.advisor.set_budget(category, amount)
                except ValueError:
                    print("Invalid amount. Please enter a number.")
            
            elif command == "view_budget":
                self.advisor.view_budget()
            
            elif command == "help":
                self.show_help()
            
            elif command == "exit":
                print("Thank you for using the Virtual Financial Advisor. Goodbye!")
                self.running = False
            
            else:
                print(f"Unknown command: {command}")
                print("Type 'help' to see available commands.")
    
    def show_help(self):
        """Display available commands"""
        print("\nAvailable Commands:")
        print("  register - Create a new user account")
        print("  login - Login to your account")
        print("  logout - Logout from your account")
        print("  add_expense - Record a new expense")
        print("  add_income - Record new income")
        print("  view_balance - View your current balance")
        print("  view_expenses - View your recent expenses")
        print("  view_income - View your recent income")
        print("  set_budget - Set a monthly budget for a category")
        print("  view_budget - View your budget and current spending")
        print("  help - Show this help menu")
        print("  exit - Exit the program")


# Run the application
if __name__ == "__main__":
    app = FinancialAdvisorCLI()
    app.run()