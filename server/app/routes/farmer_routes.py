from flask import Blueprint, request, jsonify
from app.models.farmer import Farmer
from app.models import db

farmer_bp = Blueprint('farmer_bp', __name__, url_prefix='/farmers')

# Get all farmers
@farmer_bp.route('/', methods=['GET'])
def get_farmers():
    farmers = Farmer.query.all()
    return jsonify([farmer.to_dict() for farmer in farmers]), 200

# Get one farmer by ID
@farmer_bp.route('/<int:id>', methods=['GET'])
def get_farmer(id):
    farmer = Farmer.query.get_or_404(id)
    return jsonify(farmer.to_dict()), 200

# Create new farmer
@farmer_bp.route('/', methods=['POST'])
def create_farmer():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing JSON payload'}), 400

    required_fields = ['name', 'email', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'error': f"Missing required fields: {', '.join(required_fields)}"}), 400

    try:
        new_farmer = Farmer(
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(new_farmer)
        db.session.commit()
        return jsonify(new_farmer.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update existing farmer
@farmer_bp.route('/<int:id>', methods=['PATCH'])
def update_farmer(id):
    farmer = Farmer.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing JSON payload'}), 400

    try:
        farmer.name = data.get('name', farmer.name)
        farmer.email = data.get('email', farmer.email)
        farmer.phone = data.get('phone', farmer.phone)

        db.session.commit()
        return jsonify(farmer.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a farmer
@farmer_bp.route('/<int:id>', methods=['DELETE'])
def delete_farmer(id):
    farmer = Farmer.query.get_or_404(id)

    try:
        db.session.delete(farmer)
        db.session.commit()
        return jsonify({'message': 'Farmer deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
