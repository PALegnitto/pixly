import os
from flask import Flask, request, render_template, jsonify, session, redirect,flash
from werkzeug.utils import secure_filename
from PIL import Image
import boto3
import botocore
from models import db, connect_db
from models import Image as Image_Table
from uuid import uuid4 as uuid

#TODO: Make template HTML for Home, Upload, Image Gallery
#TODO: Organize code nicely
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

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("home.html")

def send_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    file_name = f"{uuid()}.jpeg"

    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file_name,
            ExtraArgs = {
                "ContentType": "image/jpeg"
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return f"{S3_LOCATION}{file_name}"
    
@app.get("/images")
def show_all_images():
    """Show all images in AWS."""
    photo_urls = db.session.query(Image_Table.photo_url).all()
    
    return render_template("image_gallery.html", photo_urls = photo_urls)
    
    

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
            file.filename = secure_filename(file.filename)
            output = send_to_s3(file, app.config["S3_BUCKET"])
            image = Image_Table(version=1,
                               photo_url=str(output))
            db.session.add(image)
            db.session.commit()
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
