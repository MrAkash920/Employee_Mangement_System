import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('employee_db.sqlite')
cursor = conn.cursor()

# Define the Employee table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        department TEXT NOT NULL,
        position TEXT NOT NULL,
        salary FLOAT NOT NULL,
        date_of_joining DATETIME NOT NULL
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()
