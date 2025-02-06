import sqlite3

# Specify the path for the UserDetails.db file
db_path = r"C:\Users\Admin\Desktop\KredlQuiz\quiz-app\DatabaseCreation\UserDetails.db"

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    domain TEXT NOT NULL,
    score REAL DEFAULT NULL,
    questions_attempted TEXT DEFAULT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("UserDetails.db and users table created successfully!")
