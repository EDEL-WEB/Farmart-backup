import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET"),
    secure=True
)

def upload_image_to_cloudinary(file):
    try:
        upload_result = cloudinary.uploader.upload(file)
        return upload_result.get("secure_url")
    except Exception as e:
        return {"error": str(e)}
