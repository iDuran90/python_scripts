from PIL import Image
from PIL.ExifTags import TAGS
from os import listdir, rename
from os.path import isfile, join

def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    print(info)
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

onlyfiles = [f for f in listdir('../Fotos') if isfile(join('../Fotos', f))]

validPhotos = []
invalidPhotos = [] 
for file in onlyfiles:
    if 'jpg' in file or 'JPG' in file or 'png' in file:
        validPhotos.append(file)
    else:
        invalidPhotos.append(file)

for photo in validPhotos:
    try:
        taken = get_exif(photo)['DateTime']
        newName = taken.replace(':', '_')
        newName = newName.replace(' ', '_')
        newName = newName + photo[-4:]
        rename(photo, newName)
    except:
        taken = get_exif(photo)['DateTime']

# print(*invalidPhotos, sep='\n')

# from subprocess import check_output

# c = check_output("Snapchat-520592963960476532.jpg".split())
# d = {}
# print(c)
# for line in c.splitlines()[:-1]:
#     spl = line.split(":",1)
#     k, v = spl
#     d[k.lstrip()] = v.strip()
# print(d)