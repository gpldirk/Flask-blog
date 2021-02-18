import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from App.config import STATIC_FOLDER
from App.ext import mail


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_image.filename)
    filename = random_hex + file_ext
    image_path = os.path.join(STATIC_FOLDER, 'images/' + filename)

    # resize the uploaded image before save it
    image_size = (250, 250)
    i = Image.open(form_image)
    i.thumbnail(image_size)
    i.save(image_path)
    return filename


def delete_image(old_filename):
    image_path = os.path.join(STATIC_FOLDER, 'images/' + old_filename)
    if os.path.exists(image_path):
        os.remove(image_path)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='lugepei1993@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{ url_for('users.reset_token', token=token, _external=True) }
If you did not make the request, then simply ignore this email and no change will be made
    '''
    mail.send(msg)

