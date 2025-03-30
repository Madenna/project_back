import cloudinary.uploader
import logging
logger = logging.getLogger(__name__)
from rest_framework import serializers

def upload_to_cloudinary(file):
    try:
        result = cloudinary.uploader.upload(file)
        return result['secure_url']
    except Exception as e:
        logger.error(f"Cloudinary upload failed: {e}")
        raise serializers.ValidationError("Upload failed. Please try again.")