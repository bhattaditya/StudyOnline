import secrets
from os import path
from PIL import Image
from flask import current_app

def save_picture(form_picture):
    """
    This will reduce the resolution a file and then save it to a specific loaction i.e 'static/profile_pics'.

    random_hex : will generate a number alpha numeric numbers
    file_ext: with help of os module, file is split to generate --> tuple(filename, extension) 
    picture: genreated filename -> random_hex.file_ext
    picture_path: path is created so that picutre can be saved to static/profile_pics sub directory
    """

    random_hex = secrets.token_hex(8)
    _, file_ext = path.splitext(form_picture.filename)
    picture = random_hex + file_ext
    picture_path = path.join(current_app.root_path, 'static/profile_pics', picture)
    output_size = (120, 120)
    pic = Image.open(form_picture)
    pic.thumbnail(output_size)
    pic.save(picture_path)

    return picture