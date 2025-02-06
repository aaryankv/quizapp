import sqlite3
from flask import Blueprint, jsonify, request
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Define the blueprint
generate_certificate_api = Blueprint('generate_certificate_api', __name__)

# Database paths
USER_DETAILS_DB = "C:/Users/kvaar/Downloads/Quiz/Quiz/DatabaseCreation/UserDetails.db"

# Template and output paths
TEMPLATE_PATH = "C:/Users/kvaar/Downloads/Quiz/Quiz/streamlit-quiz-app/KredlCertificate.jpg"
OUTPUT_DIR = "C:/Users/kvaar/Downloads/Quiz/Certificates/"

# Function to generate a certificate
def create_certificate(name, score, date, output_path):
    try:
        # Open the certificate template
        image = Image.open(TEMPLATE_PATH)
        draw = ImageDraw.Draw(image)

        # Load fonts (ensure the .ttf file exists on your system or provide a path)
        name_font = ImageFont.truetype("arial.ttf", 100)  # Adjust font size if needed
        score_font = ImageFont.truetype("arial.ttf", 90)
        date_font = ImageFont.truetype("arial.ttf", 50)

        # Add name to the certificate
        name_position = (800, 715)  # Adjusted for the "valuable contribution of" area
        draw.text(name_position, name, font=name_font, fill="black", anchor="mm")

        # Add score to the certificate
        score_position = (1500, 940)  # Adjusted for the "Congratulations on Scoring" area
        draw.text(score_position, str(score), font=score_font, fill="black", anchor="mm")

        # Add date to the certificate
        date_position = (480, 1140)  # Adjusted for the "Date" area
        draw.text(date_position, date, font=date_font, fill="black", anchor="mm")

        # Save the generated certificate
        image.save(output_path)
        return True, output_path

    except Exception as e:
        return False, str(e)

# API endpoint to generate a certificate
@generate_certificate_api.route('/api/generate-certificate', methods=['POST'])
def generate_certificate():
    try:
        # Get data from the request
        data = request.get_json()
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        # Connect to the UserDetails database
        conn = sqlite3.connect(USER_DETAILS_DB)
        cursor = conn.cursor()

        # Fetch user details and score
        cursor.execute('''
            SELECT name, score 
            FROM users 
            WHERE id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({"error": "User not found"}), 404

        # Extract user details
        name, score = result

        # Generate the certificate
        current_date = datetime.now().strftime("%d-%b-%Y")
        output_path = f"{OUTPUT_DIR}Certificate_{user_id}.jpg"
        success, result = create_certificate(name, score, current_date, output_path)

        if success:
            return jsonify({"message": "Certificate generated successfully", "certificate_path": result}), 200
        else:
            return jsonify({"error": result}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
