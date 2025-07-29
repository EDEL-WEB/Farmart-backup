# app/routes/payment_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Order, Payment
from datetime import datetime

payment_bp = Blueprint("payment_bp", __name__)

@payment_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()

    # Get the pending order for this user
    order = Order.query.filter_by(user_id=user_id, status="pending").first()
    if not order:
        return jsonify({"error": "No pending order found"}), 404

    # Mark the order as paid
    order.status = "paid"
    order.updated_at = datetime.utcnow()

    # Create payment record
    payment = Payment(
        user_id=user_id,
        order_id=order.id,
        amount=order.total_price,
        payment_status="success",
        payment_method="simulated",
        paid_at=datetime.utcnow()
    )

    db.session.add(payment)
    db.session.commit()

    return jsonify({
        "message": "Payment successful",
        "order_id": order.id,
        "amount": order.total_price
    }), 200
