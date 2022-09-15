import os
from flask import Flask, request, render_template, jsonify, session, redirect
from werkzeug.utils import secure_filename
from PIL import Image
import boto3
import botocore
from models import db, connect_db
from models import Image as ImageDB

app = Flask(__name__)

S3_LOCATION = os.environ['S3_LOCATION']
S3_BUCKET = os.environ['S3_BUCKET']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

app.config["SECRET_KEY"] = "this-is-secret"
app.config['S3_BUCKET'] = S3_BUCKET
app.config['S3_LOCATION'] = S3_LOCATION


s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)


def send_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            "test",
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return f"{S3_LOCATION}{file.filename}"

@app.get("/")
def homepage():
    """Show homepage."""
    return """
    <!doctype html>
    <title>Home</title>
    <h1>Where you want to be</h1>
    """

@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    """Upload an image to AWS bucket and add info to db"""


    if request.method == 'POST':
        print("this is req.files:", request.files)
        if "user_file" not in request.files:
            return "No user_file key in request.files"

        file = request.files["user_file"]

        if file.filename == "":
            return "Please select a file"

        if file:
            file.filename = secure_filename(file.filename)
            output = send_to_s3(file, app.config["S3_BUCKET"])
            return str(output)

        else:
            return redirect("/")

    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=user_file>
      <input type=submit value=Upload>
    </form>
    """

# @app.patch("/api/edit-image")
# def edit_image():
#     """Edit an image stored in db"""



@app.get("/images")
def show_all_images():
    """Show all images in AWS."""


# @app.get("/search")
# def search_images():
#     """Search images based on EXIF data in database"""

""" Pillow Module ExifTags
    https://pillow.readthedocs.io/en/stable/reference/ExifTags.html#module-PIL.ExifTags
    Generates plaintext strings from hex EXIF tags

    Image.getexif()
    to get EXIF data
"""

""" Code for uploading a file

    bucket = 'your-bucket-name'
    file_name = 'location-of-your-file'
    key_name = 'name-of-file-in-s3'
    s3.upload_file(file_name, bucket, key_name)

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
"""
