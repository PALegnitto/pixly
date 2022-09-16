# TODO: get exif data from an image...yeah

from PIL import ExifTags, Image
import codecs


img = Image.open("Canon_40D.jpeg")

print("THIS IS IMAGE:",img)

exif_data = img._getexif()

print("THIS IS RAW EXIF DATA:",exif_data)

exif = {
    ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in ExifTags.TAGS
}

for tag in exif:
    print("THIS IS FORMATTED EXIF DATA",tag,":", exif[tag], type(exif[tag]))

# decoded_bulshit = codecs.decode(binary_bulshit)

# print(decoded_bulshit, 'we decoded nothing ya')