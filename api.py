from flask import Blueprint, jsonify, request

api_bp = Blueprint('api_unique', __name__, url_prefix='/api')

@api_bp.route('/status', methods=['GET'])
def api_status():
    return jsonify({"status": "success", "message": "Nsongwa Credit Union API is running!"}), 200

from flask_jwt_extended import create_access_token

@api_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    
    # Replace this with your actual User model verification logic
    if email == "chifru19@googlemail.com" and password == "securepassword":
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
        
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401
