import sqlite3

# Path to your QuizAnswers.db database
db_path = 'C:/Users/kvaar/Downloads/Quiz/Quiz/DatabaseCreation/QuizAnswers.db'

def print_all_data():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Select all data from the quiz_answers table
        cursor.execute('SELECT * FROM quiz_answers')

        # Fetch all rows
        rows = cursor.fetchall()

        # Check if data is available
        if rows:
            print("Data from quiz_answers table:")
            for row in rows:
                print(f"User ID: {row[1]}, Question ID: {row[2]}, Selected Option: {row[3]}")
        else:
            print("No data found in the quiz_answers table.")

        # Close the connection
        conn.close()

    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")

# Print all data from quiz_answers table
print_all_data()
