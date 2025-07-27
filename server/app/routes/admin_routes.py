# app/routes/admin_routes.py

from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.admin_controller import get_all_users, toggle_admin, get_user_by_id
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/admin")

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def all_users():
    return get_all_users()

@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
@admin_required
def single_user(user_id):
    return get_user_by_id(user_id)

@admin_bp.route("/users/<int:user_id>/toggle-admin", methods=["PATCH"])
@jwt_required()
@admin_required
def make_admin(user_id):
    return toggle_admin(user_id)
