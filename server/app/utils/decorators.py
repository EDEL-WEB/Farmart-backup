from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "farmer":
            return jsonify({"error": "Admins (farmers) only"}), 403
        return fn(*args, **kwargs)
    return wrapper

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "user":
            return jsonify({"error": "Users (buyers) only"}), 403
        return fn(*args, **kwargs)
    return wrapper
