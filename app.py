import os
from flask import Flask, request, render_template, jsonify, session, redirect,flash
from werkzeug.utils import secure_filename
from PIL import Image
import boto3
import botocore
from models import db, connect_db
from models import Image as Image_Table
from helpers import send_to_s3, unpack_exif_data, upload_exif_data
import pdb
import copy


#TODO: EXIF relational db and search if able; ask about EXIF data wanted

app = Flask(__name__)

S3_LOCATION = os.environ['S3_LOCATION']
S3_BUCKET = os.environ['S3_BUCKET']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

app.config["SECRET_KEY"] = "this-is-secret"
app.config['S3_BUCKET'] = S3_BUCKET
app.config['S3_LOCATION'] = S3_LOCATION
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///pixly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()



@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("home.html")


@app.get("/images")
def show_all_images():
    """Show all images in AWS."""
    photo_urls = db.session.query(Image_Table.photo_url).all()

    return render_template("image_gallery.html", photo_urls = photo_urls)


# @app.get("/images/<int:image_id>")
# def show_image(image_id):
#     """Show an image from AWS."""
#     image = Image.query.get_or_404(image_id)

#     return render_template("image_editing.html", image = image)


@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    """Upload an image to AWS bucket and add info to db"""

    if request.method == 'POST':

        if "user_file" not in request.files:
            return "No user_file key in request.files"

        file = request.files["user_file"]

        if file.filename == "":
            return "Please select a file"

        if file:
            exif_data = unpack_exif_data(file)
            file.seek(0)
            output = send_to_s3(file, app.config["S3_BUCKET"])
           
            image = Image_Table(photo_url=str(output))
            db.session.add(image)
            db.session.commit()

            db.session.refresh(image)
            print("the image id is:", image.id)
            upload_exif_data(photo_id=image.id, exif = exif_data)

            flash("Image uploaded")
            return redirect("/")

    return render_template("upload.html")


####################################

# @app.patch("/api/edit-image")
# def edit_image():
#     """Edit an image stored in db"""



# @app.get("/search")
# def search_images():
#     """Search images based on EXIF data in database"""
""" Pillow Module ExifTags
    https://pillow.readthedocs.io/en/stable/reference/ExifTags.html#module-PIL.ExifTags
    Generates plaintext strings from hex EXIF tags

    Image.getexif()
    to get EXIF data
"""
