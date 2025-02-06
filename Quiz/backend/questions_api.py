import sqlite3
from flask import Blueprint, jsonify, request

questions_api = Blueprint('questions_api', __name__)

# Function to get the domain for a specific user from the UserDetails database
def get_user_domain(user_id):
    try:
        conn = sqlite3.connect(r"C:\Users\kvaar\Downloads\Quiz\Quiz\DatabaseCreation\UserDetails.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT domain FROM users WHERE id = ?", (user_id,))
        user_domain = cursor.fetchone()
        
        conn.close()
        
        if user_domain:
            return user_domain[0]  # Return the domain (e.g., Engineering, Student, etc.)
        else:
            return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

# Function to fetch random questions from the respective domain's database
def get_questions(domain, difficulty, limit):
    db_paths = {
        "Engineering": r"C:\Users\kvaar\Downloads\Quiz\Quiz\DatabaseCreation\Engineering.db",
        # Add paths for other domains here (e.g., Science, Arts, etc.)
    }
    
    if domain not in db_paths:
        return []
    
    try:
        conn = sqlite3.connect(db_paths[domain])
        cursor = conn.cursor()
        
        cursor.execute(
            f"SELECT * FROM questions WHERE difficulty = ? ORDER BY RANDOM() LIMIT ?",
            (difficulty, limit)
        )
        questions = cursor.fetchall()
        
        conn.close()
        
        # Format questions into JSON-compatible dictionaries
        return [
            {
                "id": q[0],
                "question": q[1],
                "option_1": q[2],
                "option_2": q[3],
                "option_3": q[4],
                "option_4": q[5],
                "correct_option": q[6],
            }
            for q in questions
        ]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

# API endpoint to generate questions for the user based on domain
@questions_api.route('/api/generate-questions', methods=['GET'])
def generate_questions():
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        
        # Validate user_id as an integer
        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({"error": "Invalid User ID"}), 400
        
        # Fetch the user's domain
        domain = get_user_domain(user_id)
        
        if not domain:
            return jsonify({"error": "User not found or domain unavailable"}), 404
        
        # Fetch random questions based on domain and difficulty
        questions = []
        for difficulty, limit in [("Easy", 10), ("Medium", 10), ("Hard", 5)]:
            questions.extend(get_questions(domain, difficulty, limit))
        
        if not questions:
            return jsonify({"error": "No questions found for the selected domain"}), 404
        
        return jsonify({"questions": questions})
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
