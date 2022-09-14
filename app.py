import os
from flask import Flask, request, render_template, jsonify, session, redirect
from werkzeug.utils import secure_filename
from PIL import Image
import boto3, botocore

app = Flask(__name__)

S3_LOCATION = os.environ['S3_LOCATION']
S3_BUCKET = os.environ['S3_BUCKET']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

app.config["SECRET_KEY"] = "this-is-secret"
app.config['S3_BUCKET'] = S3_BUCKET
app.config['S3_LOCATION'] =  S3_LOCATION


s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)
""" Code for uploading a file

    bucket = 'your-bucket-name'
    file_name = 'location-of-your-file'
    key_name = 'name-of-file-in-s3'
    s3.upload_file(file_name, bucket, key_name)

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
"""

""" Pillow Module ExifTags
    https://pillow.readthedocs.io/en/stable/reference/ExifTags.html#module-PIL.ExifTags
    Generates plaintext strings from hex EXIF tags

    Image.getexif()
    to get EXIF data
"""

def send_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type    #Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(S3_LOCATION, file.filename)

@app.get("/")
def homepage():
    """Show homepage."""

@app.get("/images")
def show_all_images():
    """Show all images in AWS."""

@app.get("/search")
def search_images():
    """Search images based on EXIF data in database"""


@app.post("/upload")
def upload_image():
    """Upload an image to AWS bucket and add info to db"""

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

@app.patch("/api/edit-image")
def edit_image():
    """Edit an image stored in db"""
