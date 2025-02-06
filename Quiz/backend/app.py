from flask import Flask, jsonify
from flask_cors import CORS
from userdetails_api import userdetails_api  # Import userdetails blueprint
from questions_api import questions_api  # Import questions blueprint
from submit_quiz import submit_quiz_api  # Import submit_quiz blueprint
from score_calculation_api import score_calculation_api  # Import score_calculation blueprint
from generate_certificate_api import generate_certificate_api  # Import certificate generation blueprint

app = Flask(__name__)

# Enable CORS for all routes in the app
CORS(app, supports_credentials=True)

# Preflight CORS handler (for OPTIONS requests)
@app.route('/api/user-details', methods=['OPTIONS'])
def options_user_details():
    response = jsonify({'message': 'Options request handled for user details'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/api/questions', methods=['OPTIONS'])
def options_questions():
    response = jsonify({'message': 'Options request handled for questions'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/api/submit-quiz', methods=['OPTIONS'])
def options_submit_quiz():
    response = jsonify({'message': 'Options request handled for quiz submission'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/api/score-calculation', methods=['OPTIONS'])
def options_score_calculation():
    response = jsonify({'message': 'Options request handled for score calculation'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/api/generate-certificate', methods=['OPTIONS'])
def options_generate_certificate():
    response = jsonify({'message': 'Options request handled for certificate generation'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

# Register the blueprints
app.register_blueprint(userdetails_api)
app.register_blueprint(questions_api)
app.register_blueprint(submit_quiz_api)  # Register the submit_quiz API
app.register_blueprint(score_calculation_api)  # Register the score_calculation API
app.register_blueprint(generate_certificate_api)  # Register the certificate generation API

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
