import os
from werkzeug.utils import secure_filename
from flask import url_for
import uuid


UPLOAD_FOLDER = 'static/uploads/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# upload image function
def upload_image(file):

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{extension}"
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        image_url = url_for('static', filename=f'uploads/images/{filename}', _external=True)

        return image_url
    else:
        return None


