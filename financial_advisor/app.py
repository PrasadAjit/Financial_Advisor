from flask import Flask, render_template, request, jsonify, redirect, url_for
from financial_advisor import FinancialAdvisor  # Import the FinancialAdvisor class

app = Flask(__name__)
advisor = FinancialAdvisor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    initial_balance = float(request.form['initial_balance'])
    if advisor.register_user(username, password, initial_balance):
        return jsonify({"success": True, "message": "User registered successfully!"})
    else:
        return jsonify({"success": False, "message": "Username already exists."})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if advisor.login(username, password):
        return jsonify({"success": True, "message": f"Welcome back, {username}!"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password."})

@app.route('/logout', methods=['POST'])
def logout():
    if advisor.logout():
        return jsonify({"success": True, "message": "Logged out successfully!"})
    else:
        return jsonify({"success": False, "message": "No user is logged in."})

@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']
    if advisor.add_expense(amount, category, description):
        return jsonify({"success": True, "message": "Expense added successfully!"})
    else:
        return jsonify({"success": False, "message": "Failed to add expense."})

@app.route('/add_income', methods=['POST'])
def add_income():
    amount = float(request.form['amount'])
    source = request.form['source']
    description = request.form['description']
    if advisor.add_income(amount, source, description):
        return jsonify({"success": True, "message": "Income added successfully!"})
    else:
        return jsonify({"success": False, "message": "Failed to add income."})

@app.route('/view_balance', methods=['GET'])
def view_balance():
    balance = advisor.view_balance()
    if balance is not None:
        return jsonify({"success": True, "balance": balance})
    else:
        return jsonify({"success": False, "message": "Failed to retrieve balance."})

@app.route('/view_expenses', methods=['GET'])
def view_expenses():
    expenses = advisor.users[advisor.current_user]["expenses"]
    return jsonify({"success": True, "expenses": expenses})

@app.route('/view_income', methods=['GET'])
def view_income():
    income = advisor.users[advisor.current_user]["income"]
    return jsonify({"success": True, "income": income})

@app.route('/set_budget', methods=['POST'])
def set_budget():
    category = request.form['category']
    amount = float(request.form['amount'])
    if advisor.set_budget(category, amount):
        return jsonify({"success": True, "message": "Budget set successfully!"})
    else:
        return jsonify({"success": False, "message": "Failed to set budget."})

@app.route('/view_budget', methods=['GET'])
def view_budget():
    budget = advisor.users[advisor.current_user]["budget"]
    return jsonify({"success": True, "budget": budget})

if __name__ == '__main__':
    app.run(debug=True)