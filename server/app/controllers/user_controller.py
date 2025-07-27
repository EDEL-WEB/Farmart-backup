from flask import request, jsonify
from app.models.user import User
from app.config import db
from flask_jwt_extended import create_access_token
from datetime import timedelta

def register_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    is_admin = data.get("is_admin", False)

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already in use"}), 400

    user = User(username=username, email=email, is_admin=is_admin)
    user.password = password

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201

def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=user.id,
        additional_claims={"is_admin": user.is_admin},
        expires_delta=timedelta(days=1)
    )

    return jsonify({"token": access_token, "user": user.to_dict(), "is_admin": user.is_admin}), 200

def get_current_user(current_user):
    return jsonify(current_user.to_dict()), 200
