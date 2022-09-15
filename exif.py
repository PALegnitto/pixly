# TODO: get exif data from an image...yeah

from PIL import ExifTags, Image
import codecs


img = Image.open("Canon_40D.jpeg")
exif_data = img._getexif()

exif = {
    ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in ExifTags.TAGS
}

binary_bulshit = exif['UserComment']

hold_my_beer = codecs.decode(binary_bulshit)

print(bool(hold_my_beer))

# decoded_bulshit = codecs.decode(binary_bulshit)

# print(decoded_bulshit, 'we decoded nothing ya')