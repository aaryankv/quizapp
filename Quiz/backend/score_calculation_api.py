import sqlite3
from flask import Blueprint, jsonify, request

score_calculation_api = Blueprint('score_calculation_api', __name__)

# Helper function to connect to a database
def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# API endpoint to calculate the user's quiz score
@score_calculation_api.route('/api/calculate-score', methods=['POST'])
def calculate_score():
    try:
        # Get data from the request
        data = request.get_json()
        user_id = data.get('user_id')
        domain = data.get('domain')  # Example: 'engineering'

        # Validate input
        if not user_id or not domain:
            return jsonify({"error": "User ID and domain are required"}), 400

        # Database paths
        engineering_db = 'C:/Users/kvaar/Downloads/Quiz/Quiz/DatabaseCreation/Engineering.db'
        quiz_answers_db = 'C:/Users/kvaar/Downloads/Quiz/Quiz/DatabaseCreation/QuizAnswers.db'
        user_details_db = 'C:/Users/kvaar/Downloads/Quiz/Quiz/DatabaseCreation/UserDetails.db'

        # Fetch questions and options from the domain-specific database
        conn = get_db_connection(engineering_db)
        cursor = conn.cursor()
        cursor.execute('SELECT id, option_1, option_2, option_3, option_4, correct_option FROM questions')
        questions_db = cursor.fetchall()
        conn.close()

        # Convert questions and correct options to a dictionary
        correct_answers = {}
        for row in questions_db:
            correct_option_key = row['correct_option']
            correct_answers[row['id']] = row[correct_option_key]  # Fetch the correct answer dynamically

        print(f"Correct Answers: {correct_answers}")

        # Fetch the user's selected answers from the QuizAnswers database
        conn = get_db_connection(quiz_answers_db)
        cursor = conn.cursor()
        cursor.execute('SELECT question_id, selected_option FROM quiz_answers WHERE user_id = ?', (user_id,))
        selected_answers = cursor.fetchall()
        conn.close()

        print(f"Selected Answers: {selected_answers}")

        # Calculate the score
        score = 0
        questions_attempted = []

        for answer in selected_answers:
            question_id = answer['question_id']
            selected_answer = answer['selected_option']
            correct_answer = correct_answers.get(question_id)

            print(f"Checking question_id: {question_id}, selected_answer: {selected_answer}, correct_answer: {correct_answer}")

            # Compare selected answer with correct answer
            if correct_answer == selected_answer:
                score += 1

            questions_attempted.append(question_id)

        total_questions_attempted = len(questions_attempted)
        print(f"Total Questions Attempted: {total_questions_attempted}")

        # Update the user's score and questions attempted in the UserDetails database
        conn = get_db_connection(user_details_db)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET score = ?, questions_attempted = ? 
            WHERE id = ?
        ''', (score, ','.join(map(str, questions_attempted)), user_id))
        conn.commit()
        conn.close()

        print(f"Final Score: {score}, Questions Attempted: {questions_attempted}")

        return jsonify({
            'message': 'Score calculated successfully',
            'score': score,
            'total_questions_attempted': total_questions_attempted
        }), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500
