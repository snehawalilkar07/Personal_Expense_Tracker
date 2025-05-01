import sqlite3 
import pandas as pd
import streamlit as st

class Expense_Manager:

    def __init__ (self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # create a table if it does not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            date DATE,
                            amount REAL,
                            category TEXT,
                            description TEXT)''')
        self.conn.commit()

    def addExpense(self, date, name, amount, category, description):
        self.cursor.execute('''INSERT INTO expenses (name, date, amount, category, description)
                           VALUES (?,?,?,?,?)''',
                            (name, date, amount, category, description))
        self.conn.commit()

    def viewExpenses(self):
        query = "SELECT * from expenses"
        return pd.read_sql(query, self.conn)
    
    def deleteExpense(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()

class Income_Manager:

    def __init__ (self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # create a table if it does not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            date DATE,
                            amount REAL,
                            category TEXT,
                            description TEXT)''')
        self.conn.commit()

    def addIncome(self, date, name, amount, category, description):
        self.cursor.execute('''INSERT INTO income (name, date, amount, category, description)
                           VALUES (?,?,?,?,?)''',
                            (name, date, amount, category, description))
        self.conn.commit()

    def viewIncome(self):
        query = "SELECT * from income"
        return pd.read_sql(query, self.conn)
    
    def deleteIncome(self, income_id):
        self.cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
        self.conn.commit()

class Account:
    def __init__(self, db_name):
        self.Income_Manager = Income_Manager(db_name)
        self.Expense_Manager = Expense_Manager(db_name)
        self.Balance = 0.0

    def getBalance(self):
        total_income = self.Income_Manager.viewIncome()["amount"].sum()
        total_expense = self.Expense_Manager.viewExpenses()["amount"].sum()
        self.Balance = total_income - total_expense
        return self.Balance
    
    def addExpense(self, date, name, amount, category, description):
        self.Expense_Manager.addExpense( date, name, amount, category, description)
        self.Balance -= amount
        st.success("Expense added Successfully!")

    def addIncome(self, date, name, amount, category, description):
        self.Income_Manager.addIncome(date, name, amount, category, description)
        self.Balance += amount
        st.success("Income added Successfully!")

    def expense_List(self):
        return self.Expense_Manager.viewExpenses()

    def income_List(self):
        return self.Income_Manager.viewIncome()

    def deleteExpense(self, expense_id):
        expenses = self.Expense_Manager.viewExpenses()
        if expenses.empty:
            st.warning("No expenses to delete.")
            return

        if expense_id in expenses["id"].values:
            amount = expenses.loc[expenses["id"] == expense_id, "amount"].values[0]
            self.Expense_Manager.deleteExpense(expense_id)
            self.Balance += amount
            st.success(f"Expense {expense_id} deleted successfully!")
        else:
            st.warning(f"Invalid Expense ID: {expense_id}")  

    def deleteIncome(self, income_id):
        income = self.Income_Manager.viewIncome()
        if income.empty:
            st.warning("No income to delete.")
            return

        if income_id in income["id"].values:
            amount = income.loc[income["id"] == income_id, "amount"].values[0]
            self.Income_Manager.deleteIncome(income_id)
            self.Balance -= amount
            st.success(f"Income {income_id} deleted successfully!")
        else:
            st.warning(f"Invalid Income ID: {income_id}")       

    # transction List
    def format_transaction(self):
        expenses = self.Expense_Manager.viewExpenses()
        income = self.Income_Manager.viewIncome()

        formatted_expenses = expenses[['name',"date","amount", "category", "description"]].to_dict(orient = "records")
        formatted_income = income[['name',"date","amount", "category", "description"]].to_dict(orient = "records")

        transactions = {
            'income':formatted_income,
            'expenses': formatted_expenses
        }
        return transactions
             
        