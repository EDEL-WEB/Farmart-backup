# app/controllers/checkout_controller.py

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.models import Order, Payment, db

@jwt_required()
def checkout():
    user_id = get_jwt_identity()

    # 1. Get the user's pending order
    order = Order.query.filter_by(user_id=user_id, status="pending").first()

    if not order:
        return jsonify({"error": "No pending order found"}), 404

    # 2. Calculate total amount
    total_amount = sum(item.animal.price for item in order.cart_items)

    # 3. Create a Payment entry
    payment = Payment(
        user_id=user_id,
        amount=total_amount,
        method="MockPay",  # Simulated method
        status="paid",
        timestamp=datetime.utcnow()
    )
    db.session.add(payment)

    # 4. Mark order as paid
    order.status = "paid"

    # 5. Commit everything
    try:
        db.session.commit()
        return jsonify({
            "message": "Checkout successful!",
            "order_id": order.id,
            "total_paid": total_amount,
            "payment_id": payment.id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
