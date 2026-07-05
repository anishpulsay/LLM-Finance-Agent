import sqlite3


def add_expense(name,amount,date,category):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    c.execute("""INSERT INTO users(name,amount,date,category)
                VALUES(?,?,?,?)""",(name,amount,date,category))
    conn.commit()
    conn.close()
    return "Expense added successfully"

def get_expenses(category = None):
    conn = sqlite3.connect('database/database.db')
    c= conn.cursor()
    if category:
        c.execute("SELECT * FROM users WHERE category = ?",
        (category,)
        )

    else:
        c.execute("SELECT * FROM users")
        items = c.fetchall()
        conn.close()
        return items 

def update_expenses(name, amount=None):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET amount = ? WHERE name = ?",(amount,name))
    conn.commit()
    conn.close()
    return "Expense Updated successfully"
