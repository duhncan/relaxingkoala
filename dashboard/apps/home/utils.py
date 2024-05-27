import os
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename


def save_picture(form_picture, output_size=(300, 300)):
    random_hex = os.urandom(8).hex()
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/assets/images/menu_pics", picture_fn
    )

    # Ensure the directory exists
    if not os.path.exists(os.path.dirname(picture_path)):
        os.makedirs(os.path.dirname(picture_path))

    # Open the image and resize it
    img = Image.open(form_picture)
    img.thumbnail(output_size)

    # Save the resized image
    img.save(picture_path)

    print(f"Saved file at location: {picture_path}")
    return picture_fn


def delete_picture(picture_name):
    picture_path = os.path.join(
        current_app.root_path, "static/assets/images/menu_pics", picture_name
    )
    if os.path.exists(picture_path):
        os.remove(picture_path)
