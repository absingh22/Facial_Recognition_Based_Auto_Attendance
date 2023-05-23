from imutils import paths
from PIL import Image, ExifTags
import os
from datetime import date

#today = date.today()
#day = today.strftime("%a")
#print(today)
#print(day)
#today = date(2020, 4, 11)
#day = today.strftime("%a")
#print(today)
#print(day)

#print("[INFO] quantifying faces...")
#imagePaths = list(paths.list_images("dataset\Dipen_Singh"))

#for (i, imagePath) in enumerate(imagePaths):
#    print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
#    name = imagePath.split(os.path.sep)[-2]
#    file = imagePath.split(os.path.sep)[-1]
#    image = Image.open(imagePath)
#
#    try :
#        for orientation in ExifTags.TAGS.keys() :
#            if ExifTags.TAGS[orientation]=='Orientation' :
#                break
#        exif=dict(image._getexif().items())
#
#        if   exif[orientation] == 3 :
#            image=image.rotate(180, expand=True)
#        elif exif[orientation] == 6 :
#            image=image.rotate(270, expand=True)
#        elif exif[orientation] == 8 :
#            image=image.rotate(90, expand=True)
#
#    except :
#        image = image
#
#    image = image.resize((1169, 1558), Image.ANTIALIAS)
#    path = "dataset-reduced\\"
#    image.save(path + name + '\\' +file)