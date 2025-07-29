from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from app.models.animal import Animal, db
import os
import uuid

animal_bp = Blueprint("animal_bp", __name__, url_prefix="/api/animals")

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# CREATE animal with optional image
@animal_bp.route("", methods=["POST"])
def create_animal():
    data = request.form
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")

    # Default image
    picture_url = None

    # Handle file upload
    if "image" in request.files:
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit(".", 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(filepath)
            picture_url = f"/{filepath}"

    animal = Animal(
        name=name,
        description=description,
        price=price,
        picture_url=picture_url
    )
    db.session.add(animal)
    db.session.commit()
    return jsonify(animal.serialize()), 201

# GET all animals
@animal_bp.route("", methods=["GET"])
def get_animals():
    animals = Animal.query.all()
    return jsonify([a.serialize() for a in animals]), 200

# GET one animal
@animal_bp.route("/<int:id>", methods=["GET"])
def get_animal(id):
    animal = Animal.query.get_or_404(id)
    return jsonify(animal.serialize()), 200

# UPDATE animal info (and optionally picture)
@animal_bp.route("/<int:id>", methods=["PATCH"])
def update_animal(id):
    animal = Animal.query.get_or_404(id)
    data = request.form

    animal.name = data.get("name", animal.name)
    animal.description = data.get("description", animal.description)
    animal.price = data.get("price", animal.price)

    if "image" in request.files:
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit(".", 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(filepath)
            animal.picture_url = f"/{filepath}"

    db.session.commit()
    return jsonify(animal.serialize()), 200

# DELETE animal
@animal_bp.route("/<int:id>", methods=["DELETE"])
def delete_animal(id):
    animal = Animal.query.get_or_404(id)
    db.session.delete(animal)
    db.session.commit()
    return jsonify({"message": "Animal deleted"}), 200
