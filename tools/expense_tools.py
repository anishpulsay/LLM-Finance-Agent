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
