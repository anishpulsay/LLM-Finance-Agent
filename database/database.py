import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                             name TEXT, 
                                             amount REAL, 
                                             Date TEXT,
                                             category TEXT )""")
conn.commit()
conn.close()

            