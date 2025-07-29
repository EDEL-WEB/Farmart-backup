from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Animal, Order  # replace Order if your model is named Purchase
from app.controllers.admin_controller import (
    get_all_users,
    get_user_by_id,
    toggle_admin
)
from functools import wraps

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/admin")

# ✅ Admin-only route decorator
def admin_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return func(*args, **kwargs)
    return wrapper

# ✅ GET /api/admin/users — Get all users
@admin_bp.route("/users", methods=["GET"])
@admin_required
def all_users():
    return get_all_users()

# ✅ GET /api/admin/users/<id> — Get a single user by ID
@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@admin_required
def single_user(user_id):
    return get_user_by_id(user_id)

# ✅ PATCH /api/admin/users/<id>/toggle-admin — Promote or demote user to/from admin
@admin_bp.route("/users/<int:user_id>/toggle-admin", methods=["PATCH"])
@admin_required
def make_admin(user_id):
    return toggle_admin(user_id)

# ✅ GET /api/admin/summary — Get admin dashboard summary
@admin_bp.route("/summary", methods=["GET"])
@admin_required
def admin_summary():
    total_users = User.query.count()
    total_animals = Animal.query.count()
    total_orders = Order.query.count()  # Replace if using Purchase

    return jsonify({
        "total_users": total_users,
        "total_animals": total_animals,
        "total_orders": total_orders
    }), 200
