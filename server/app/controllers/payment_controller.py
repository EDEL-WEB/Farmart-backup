from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Order, Payment, User
from app.extensions import db
from datetime import datetime

@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    
    # Step 1: Get the pending order
    order = Order.query.filter_by(user_id=user_id, status="pending").first()
    if not order:
        return jsonify({"error": "No pending order found"}), 404

    # Step 2: Calculate total amount
    total = sum(item.animal.price for item in order.items)  # Ensure `order.items` relationship exists

    # Step 3: Create the payment
    payment = Payment(
        order_id=order.id,
        user_id=user_id,
        farmer_id=order.items[0].animal.farmer_id if order.items else None,  # Optional
        amount=total,
        method=request.json.get("method", "Mpesa"),
        status="paid",  # Simulate successful payment
        created_at=datetime.utcnow()
    )
    db.session.add(payment)

    # Step 4: Mark order as completed
    order.status = "completed"
    
    try:
        db.session.commit()
        return jsonify({"message": "Checkout successful", "payment": payment.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
