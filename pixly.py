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
