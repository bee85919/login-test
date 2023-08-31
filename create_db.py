import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Drop table if exists
c.execute("DROP TABLE IF EXISTS users")

# Create new table
c.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              email TEXT NOT NULL UNIQUE,
              token TEXT NOT NULL,
              verified INTEGER DEFAULT 0);''')

conn.commit()
conn.close()