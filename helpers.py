import os
from PIL import ExifTags, Image
import codecs
from uuid import uuid4 as uuid
import boto3
from models import db
from models import ExifData

S3_LOCATION = os.environ['S3_LOCATION']
S3_BUCKET = os.environ['S3_BUCKET']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

def send_to_s3(file, bucket_name, s3_loc):
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

    return f"{s3_loc}{file_name}"

def unpack_exif_data(picture):
    """ unpacks the exif data when user uploads image"""

    img = Image.open(picture)
    exif_data = img._getexif()

    if not exif_data:
        info_dict = {"Image Size": img.size,
                    "Image Height": img.height,
                    "Image Width": img.width,
                    "Image Format": img.format,}
        return info_dict

    else:
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in ExifTags.TAGS
        }

        return exif
        

def upload_exif_data(photo_id, exif):
    """ adds exif data to the database"""

    for tag in exif:
        entry = ExifData(photo_id = photo_id, tag = tag, value = str(exif[tag]))
        db.session.add(entry)

    db.session.commit()



