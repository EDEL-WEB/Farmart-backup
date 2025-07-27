from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import register_user, login_user

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    return register_user(request.json)

@auth_bp.route("/login", methods=["POST"])
def login():
    return login_user(request.json)
