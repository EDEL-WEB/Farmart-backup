from flask import Blueprint, request, jsonify
from app.models.cart import Cart, db
from app.models.animal import Animal

# Blueprint registration
cart_bp = Blueprint('cart_bp', __name__, url_prefix='/api/cart')

# Add an animal to cart
@cart_bp.route('/', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    user_id = data.get('user_id')
    animal_id = data.get('animal_id')

    if not user_id or not animal_id:
        return jsonify({'error': 'user_id and animal_id are required'}), 400

    animal = Animal.query.get(animal_id)
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404
    if animal.is_sold:
        return jsonify({'error': 'Animal is already sold'}), 400

    # Check if animal is already in the user's cart
    existing = Cart.query.filter_by(user_id=user_id, animal_id=animal_id).first()
    if existing:
        return jsonify({'error': 'Animal already in cart'}), 409

    # Add new item to cart
    new_item = Cart(user_id=user_id, animal_id=animal_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_dict()), 201

# Get all cart items for a user
@cart_bp.route('/', methods=['GET'])
def get_user_cart():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    cart_data = []

    for item in cart_items:
        animal = Animal.query.get(item.animal_id)
        if animal:
            cart_data.append({
                "cart_id": item.id,
                "user_id": item.user_id,
                "animal": animal.to_dict()
            })

    return jsonify(cart_data), 200

# Remove a specific item from the cart
@cart_bp.route('/<int:item_id>', methods=['DELETE'])
def remove_item(item_id):
    item = Cart.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'}), 200

# Clear the entire cart for a user
@cart_bp.route('/clear', methods=['DELETE'])
def clear_cart():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    items = Cart.query.filter_by(user_id=user_id).all()
    for item in items:
        db.session.delete(item)

    db.session.commit()
    return jsonify({'message': 'Cart cleared'}), 200

# Checkout all items in the cart and mark animals as sold
@cart_bp.route('/checkout', methods=['POST'])
def checkout_cart():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    sold_animals = []
    for item in cart_items:
        animal = Animal.query.get(item.animal_id)
        if animal and not animal.is_sold:
            animal.is_sold = True
            sold_animals.append(animal.to_dict())
        db.session.delete(item)

    db.session.commit()

    return jsonify({
        "message": f"{len(sold_animals)} animals checked out",
        "sold_animals": sold_animals
    }), 200
