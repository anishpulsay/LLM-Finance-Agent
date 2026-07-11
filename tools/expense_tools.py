from collections import UserString
import sqlite3
from datetime import date


def add_expense(name,amount,expense_date = None,category = None):
    if not expense_date:
        expense_date = date.today().isoformat()
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    c.execute("""INSERT INTO users(name,amount,date,category)
                VALUES(?,?,?,?)""",(name,amount,expense_date,category))
    conn.commit()
    conn.close()
    return "Expense added successfully"

def get_expenses(category = None, expense_date = None):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    query = "SELECT * FROM users WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if expense_date:
        query += " AND date = ?"
        params.append(expense_date)
    c.execute(query, tuple(params))
    items = c.fetchall()
    conn.close()
    return items 

def get_current_date():
    return date.today().isoformat() 

def update_expenses(name, amount=None):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET amount = ? WHERE name = ?",(amount,name))
    conn.commit()
    conn.close()
    return "Expense Updated successfully"

def delete_expense(expense_id):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?",(expense_id,))
    conn.commit()
    conn.close()
    return "Deleted expense successfully"

def financial_summary(name = None,category = None,start_date = None,end_date = None):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    query = "SELECT * FROM users WHERE 1 = 1"
    params = []
    if name:
        query += " AND name = ?"
        params.append(name)
    if category:
        query += " AND category = ?"
        params.append(category)
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    c.execute(query,params)
    expenses = c.fetchall()
    conn.close()
    if not expenses:
        return{
            "message" : "No expense found"
        }
    total_spent = sum(expense[2] for expense in expenses)
    highest_expense = max(expense[2] for expense in expenses)
    lowest_expense = min(expense[2] for expense in expenses)
    return {
        "total_spent": total_spent,
        "highest_expense": highest_expense,
        "lowest_expense": lowest_expense,
        "count": len(expenses)
    }





