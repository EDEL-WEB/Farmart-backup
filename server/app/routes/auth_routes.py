from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    unset_jwt_cookies,
    set_access_cookies
)
from datetime import timedelta
from app.models.user import User
from app.extensions import db
import logging
import re
import traceback

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

# ---------- Routes ----------

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return _build_preflight_response()
    return register_user()

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return _build_preflight_response()
    return login_user()

@auth_bp.route('/check_session', methods=['GET', 'OPTIONS'])
@jwt_required()
def check_session_route():
    if request.method == 'OPTIONS':
        return _build_preflight_response()
    return check_session()

@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
@jwt_required()
def logout():
    if request.method == 'OPTIONS':
        return _build_preflight_response()
    return logout_user()

# ---------- CORS Helpers ----------

def _build_preflight_response():
    response = jsonify({"message": "Preflight OK"})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    return response

def _add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# ---------- Controllers ----------

def register_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "farmer")

        if not all([username, email, password]):
            return jsonify({"error": "Missing required fields"}), 400

        if len(password) < 6:
            return jsonify({"error": "Password too short"}), 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Invalid email"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email exists"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username taken"}), 400

        user = User(username=username, email=email, role=role)
        user.password = password  # uses hybrid_property for hashing
        db.session.add(user)
        db.session.commit()

        response = jsonify({
            "message": "Registration successful",
            "user": user.to_dict()
        })
        return _add_cors_headers(response), 201

    except Exception as e:
        db.session.rollback()
        logger.error("Registration error: %s\n%s", str(e), traceback.format_exc())
        return jsonify({"error": "Registration failed"}), 500

def login_user():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing credentials"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(days=1)
        )

        response = jsonify({
            "message": "Login successful",
            "user": user.to_dict(),
            "access_token": access_token
        })
        set_access_cookies(response, access_token)
        # return response
        return _add_cors_headers(response)

    except Exception as e:
        logger.error("Login error: %s\n%s", str(e), traceback.format_exc())
        return jsonify({"error": "Login failed"}), 500

def check_session():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        response = jsonify({
            "message": "Session valid",
            "user": user.to_dict()
        })
        return _add_cors_headers(response)

    except Exception as e:
        logger.error("Check session error: %s\n%s", str(e), traceback.format_exc())
        return jsonify({"error": "Session check failed"}), 500

def logout_user():
    try:
        response = jsonify({"message": "Logout successful"})
        unset_jwt_cookies(response)
        return _add_cors_headers(response)
    except Exception as e:
        logger.error("Logout error: %s\n%s", str(e), traceback.format_exc())
        return jsonify({"error": "Logout failed"}), 500
