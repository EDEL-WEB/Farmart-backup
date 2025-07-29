from flask import Blueprint
from app.controllers.order_controller import (
    create_order,
    get_all_orders,
    get_order,
    update_order_status,
    delete_order,
)
from flask_jwt_extended import jwt_required

order_bp = Blueprint("order_bp", __name__, url_prefix="/api/orders")

@order_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    return create_order()

@order_bp.route("/", methods=["GET"])
@jwt_required()
def get_all():
    return get_all_orders()

@order_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_one(order_id):
    return get_order(order_id)

@order_bp.route("/<int:order_id>", methods=["PATCH"])
@jwt_required()
def update(order_id):
    return update_order_status(order_id)

@order_bp.route("/<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete(order_id):
    return delete_order(order_id)
