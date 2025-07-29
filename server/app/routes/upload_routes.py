# app/routes/upload_routes.py

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid

from app.models.animal import Animal, db  # adjust if needed

upload_bp = Blueprint('upload_bp', __name__, url_prefix='/api/animals')

@upload_bp.route('/upload', methods=['POST'])
def upload_animal_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    name = request.form.get('name')
    breed = request.form.get('breed')
    description = request.form.get('description')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[-1].lower()
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(current_app.root_path, 'static/uploads', new_filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)

        # Save animal with picture_url path
        picture_url = f"/static/uploads/{new_filename}"
        animal = Animal(name=name, breed=breed, description=description, picture_url=picture_url)
        db.session.add(animal)
        db.session.commit()

        return jsonify({'message': 'Animal uploaded successfully', 'animal': animal.serialize()}), 201

    return jsonify({'error': 'File upload failed'}), 500
