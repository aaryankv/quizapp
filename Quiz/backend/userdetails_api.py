import sqlite3
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin  # Importing cross_origin to handle CORS issues

userdetails_api = Blueprint('userdetails_api', __name__)

# Function to add user details to the database
@userdetails_api.route('/api/user-details', methods=['POST'])
@cross_origin()  # Allow cross-origin requests for this route
def add_user_details():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    contact_number = data.get('contact_number')
    domain = data.get('domain')
    
    if not name or not email or not contact_number or not domain:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Insert user details into the database
    conn = sqlite3.connect(r"C:\Users\kvaar\Downloads\Quiz\Quiz\DatabaseCreation\UserDetails.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name, email, contact_number, domain) VALUES (?, ?, ?, ?)",
                   (name, email, contact_number, domain))
    conn.commit()
    
    # Get the last inserted user ID
    user_id = cursor.lastrowid
    
    conn.close()
    
    return jsonify({"message": "User details added", "user_id": user_id}), 201

# Function to fetch all users (if needed)
@userdetails_api.route('/api/users', methods=['GET'])
@cross_origin()  # Allow cross-origin requests for this route
def get_all_users():
    conn = sqlite3.connect(r"C:\Users\kvaar\Downloads\Quiz\Quiz\DatabaseCreation\UserDetails.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    conn.close()
    
    # Format the users list to improve response readability
    formatted_users = []
    for user in users:
        formatted_users.append({
            'user_id': user[0],
            'name': user[1],
            'email': user[2],
            'contact_number': user[3],
            'domain': user[4]
        })
    
    return jsonify({"users": formatted_users})

