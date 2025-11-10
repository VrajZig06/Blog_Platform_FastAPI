import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv
from fastapi import UploadFile

load_dotenv()

print(os.getenv("CLOUF_NAME"))

cloudinary.config( 
  cloud_name = os.getenv('CLOUD_NAME'), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

def upload_file_to_cloudinary(file: UploadFile):
    try:
        if not file:
            return None

        upload_result = cloudinary.uploader.upload(file.file, folder="blogify_uploads")

        return upload_result.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload failed: {e}")
        return None