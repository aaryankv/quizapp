import sqlite3
from flask import Blueprint, jsonify, request

submit_quiz_api = Blueprint('submit_quiz_api', __name__)

# API endpoint to submit quiz answers and store them in the QuizAnswers database
@submit_quiz_api.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    try:
        # Get data from the request
        data = request.get_json()

        # Validate input
        user_id = data.get("user_id")  # The key should match the request body (user_id)
        user_answers = data.get("answers")

        if not user_id or not user_answers:
            return jsonify({"error": "User ID and answers are required"}), 400

        # Connect to the QuizAnswers database to insert answers
        conn = sqlite3.connect('C:/Users/kvaar/Downloads/Quiz/Quiz/DatabaseCreation/QuizAnswers.db')  # Update path as necessary
        cursor = conn.cursor()

        # Insert each answer into the quiz_answers table
        for question_id, selected_option in user_answers.items():
            cursor.execute('''
                INSERT INTO quiz_answers (user_id, question_id, selected_option)
                VALUES (?, ?, ?)
            ''', (user_id, question_id, selected_option))

        # Commit the transaction to save the answers
        conn.commit()
        conn.close()

        return jsonify({"message": "Answers submitted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
