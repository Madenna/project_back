import cloudinary.uploader

def upload_to_cloudinary(file):
    result = cloudinary.uploader.upload(file)
    return result['secure_url']