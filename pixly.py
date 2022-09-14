import os
from flask import Flask, request, render_template, jsonify, session
from PIL import Image
import boto3

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)
""" Code for uploading a file

    bucket = 'your-bucket-name'
    file_name = 'location-of-your-file'
    key_name = 'name-of-file-in-s3'
    client.upload_file(file_name, bucket, key_name)
    
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
"""

""" Pillow Module ExifTags
    https://pillow.readthedocs.io/en/stable/reference/ExifTags.html#module-PIL.ExifTags
    Generates plaintext strings from hex EXIF tags
    
    Image.getexif()
    to get EXIF data
"""

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
    
@app.patch("/api/edit-image")
def edit_image():
    """Edit an image stored in db"""
