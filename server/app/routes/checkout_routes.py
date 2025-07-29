from flask import Blueprint
from app.controllers.checkout_controller import checkout

checkout_bp = Blueprint("checkout_bp", __name__)

checkout_bp.route("/checkout", methods=["POST"])(checkout)
