import sqlite3

def create_answers_database():
    # Connect to SQLite database (it will create the database if it doesn't exist)
    conn = sqlite3.connect('QuizAnswers.db')
    cursor = conn.cursor()

    # Create a table to store user answers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question_id INTEGER,
            selected_option TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')

    conn.commit()
    conn.close()

    print("QuizAnswers database and table created successfully!")

# Call the function to create the database and table
create_answers_database()
