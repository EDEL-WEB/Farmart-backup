from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.payment import Payment
from app.controllers.payment_controller import PaymentController, PaymentControllerOne

payment_bp = Blueprint("payment_bp", __name__)

# Instantiate your controllers
payment_controller = PaymentController()
payment_controller_one = PaymentControllerOne()

# GET all payments
@payment_bp.route("/payments", methods=["GET"])
@jwt_required()
def get_payments():
    return payment_controller.get_all()

# GET one payment by ID
@payment_bp.route("/payments/<int:id>", methods=["GET"])
@jwt_required()
def get_payment(id):
    return payment_controller_one.get_one(id)

# CREATE a payment
@payment_bp.route("/payments", methods=["POST"])
@jwt_required()
def create_payment():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = current_user_id  # Optional: if payments are tied to users
    return payment_controller.create(data)

# UPDATE a payment
@payment_bp.route("/payments/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_payment(id):
    data = request.get_json()
    return payment_controller.update(id, data)

# DELETE a payment
@payment_bp.route("/payments/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_payment(id):
    return payment_controller.delete(id)
