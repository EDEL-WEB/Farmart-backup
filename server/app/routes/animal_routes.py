import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from flask_cors import CORS

from app.models import db, Animal, User

animal_bp = Blueprint("animal_bp", __name__, url_prefix="/api/animals")
CORS(animal_bp, supports_credentials=True, origins=["http://localhost:3000"])

UPLOAD_FOLDER = os.path.join("app", "static", "images", "animals")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@animal_bp.route("/", methods=["OPTIONS"])
def animals_options():
    response = jsonify({"message": "CORS preflight passed"})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 204


@animal_bp.route("/", methods=["GET"])
def get_animals():
    animals = Animal.query.all()
    return jsonify([a.to_dict() for a in animals]), 200


@animal_bp.route("/<int:id>", methods=["GET"])
def get_animal(id):
    animal = Animal.query.get_or_404(id)
    return jsonify(animal.to_dict()), 200


@animal_bp.route("/", methods=["POST", "OPTIONS"])
@jwt_required()
def create_animal():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    if user.role != "farmer":
        return jsonify({"error": "Only farmers can upload animals"}), 403

    name = request.form.get("name")
    breed = request.form.get("breed")
    age = request.form.get("age")
    price = request.form.get("price")
    description = request.form.get("description")
    animal_type = request.form.get("type")
    file = request.files.get("image")

    if not all([name, breed, age, price, animal_type, file]):
        return jsonify({"error": "Missing required fields"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    file.save(image_path)

    try:
        new_animal = Animal(
            name=name,
            breed=breed,
            age=int(age),
            price=float(price),
            description=description,
            picture_url=f"/static/images/animals/{filename}",
            farmer_id=user.id,
            user_id=user.id,
            type=animal_type,
        )
        db.session.add(new_animal)
        db.session.commit()

        response = jsonify(new_animal.to_dict())
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 201

    except Exception as e:
        db.session.rollback()
        print("Error during animal upload:", e)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@animal_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_animal(id):
    animal = Animal.query.get_or_404(id)
    user_id = get_jwt_identity()

    if animal.farmer_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    name = request.form.get("name", animal.name)
    breed = request.form.get("breed", animal.breed)
    age = request.form.get("age", animal.age)
    price = request.form.get("price", animal.price)
    description = request.form.get("description", animal.description)
    animal_type = request.form.get("type", animal.type)
    file = request.files.get("image")

    if file:
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid image format"}), 400
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        animal.picture_url = f"/static/images/animals/{filename}"

    animal.name = name
    animal.breed = breed
    animal.age = int(age)
    animal.price = float(price)
    animal.description = description
    animal.type = animal_type

    db.session.commit()
    return jsonify(animal.to_dict()), 200


@animal_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_animal(id):
    animal = Animal.query.get_or_404(id)
    user_id = get_jwt_identity()

    if animal.farmer_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(animal)
    db.session.commit()
    return jsonify({"message": "Animal deleted"}), 200
