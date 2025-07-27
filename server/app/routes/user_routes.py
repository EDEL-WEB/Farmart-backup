from flask import Blueprint
from app.controllers.user_controller import register_user, login_user, get_current_user
from app.utils.decorators import jwt_user_required

user_bp = Blueprint("user_bp", __name__, url_prefix="/api/users")

user_bp.route("/register", methods=["POST"])(register_user)
user_bp.route("/login", methods=["POST"])(login_user)
user_bp.route("/profile", methods=["GET"])(jwt_user_required(get_current_user))
