from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.animal import Animal, db
from app.models.user import User
from PIL import Image
import cloudinary.uploader
import io
from werkzeug.utils import secure_filename

animal_bp = Blueprint('animal_bp', __name__, url_prefix='/animals')

# GET /animals - Get all animals with optional filters
@animal_bp.route('/', methods=['GET'])
def get_animals():
    query = Animal.query
    breed = request.args.get('breed')
    age = request.args.get('age')
    animal_type = request.args.get('type')

    if breed:
        query = query.filter_by(breed=breed)
    if age:
        query = query.filter_by(age=int(age))
    if animal_type:
        query = query.filter_by(type=animal_type)

    animals = [animal.to_dict() for animal in query.all()]
    return jsonify(animals), 200

# GET /animals/<id> - Get animal by ID
@animal_bp.route('/<int:id>', methods=['GET'])
def get_animal(id):
    animal = Animal.query.get_or_404(id)
    return jsonify(animal.to_dict()), 200

# POST /animals - Create a new animal (Farmer only)
@animal_bp.route('/', methods=['POST'])
@jwt_required()
def create_animal():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    if user.role != 'farmer':
        return jsonify({'error': 'Only farmers can add animals'}), 403

    if 'picture' not in request.files:
        return jsonify({'error': 'Picture file is required'}), 400

    file = request.files['picture']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Process image
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((600, 400))

        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)

        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            buffer,
            folder="farmart/animals",
            public_id=secure_filename(file.filename.rsplit('.', 1)[0]),
            overwrite=True,
            resource_type="image"
        )

        # Get form data
        name = request.form.get('name')
        breed = request.form.get('breed')
        age = request.form.get('age')
        price = request.form.get('price')
        animal_type = request.form.get('type')

        if not all([name, breed, age, price, animal_type]):
            return jsonify({'error': 'Missing required fields'}), 400

        new_animal = Animal(
            name=name,
            breed=breed,
            age=int(age),
            price=float(price),
            type=animal_type,
            farmer_id=user.id,
            picture_url=upload_result['secure_url']
        )
        db.session.add(new_animal)
        db.session.commit()

        return jsonify(new_animal.to_dict()), 201

    except Exception as e:
        return jsonify({'error': f'Image upload failed: {str(e)}'}), 500

# PATCH /animals/<id> - Update animal (Farmer only, owns animal)
@animal_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def update_animal(id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    animal = Animal.query.get_or_404(id)

    if user.role != 'farmer' or animal.farmer_id != user.id:
        return jsonify({'error': 'Unauthorized to update this animal'}), 403

    data = request.get_json()
    for field in ['name', 'breed', 'age', 'price', 'type', 'is_sold']:
        if field in data:
            setattr(animal, field, data[field])

    db.session.commit()
    return jsonify(animal.to_dict()), 200

# DELETE /animals/<id> - Delete animal (Farmer only, owns animal)
@animal_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_animal(id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    animal = Animal.query.get_or_404(id)

    if user.role != 'farmer' or animal.farmer_id != user.id:
        return jsonify({'error': 'Unauthorized to delete this animal'}), 403

    db.session.delete(animal)
    db.session.commit()
    return jsonify({'message': 'Animal deleted successfully'}), 200
