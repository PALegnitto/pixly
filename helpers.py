from PIL import ExifTags, Image
import codecs

def unpack_exif_data(picture):
    """ unpacks the exif data when user uploads image"""

    img = Image.open(picture)
    exif_data = img._getexif()


    exif = {
        ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in ExifTags.TAGS
    }

    return exif

def add_image_to_db(exif):
    """ adds exif datat to the database"""

    for tag in exif:
        ExifData ()




