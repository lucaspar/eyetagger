# Manual migrations to import dataset. Used to populate the database,
#   like fixtures, but with custom real data. Follow the steps below:

# 0. Create an empty migration file with:
#       python manage.py makemigrations --empty api

# 1. From the created file, import this one like below:
#     from backend.api.manual_migration import import_dataset

# 2. Then inside the created file, in the Migration class, paste the following:

#     initial = True
#     operations = [
#         migrations.RunPython(import_dataset, reverse_code=migrations.RunPython.noop)
#     ]

from django.db import migrations, models
from django.conf import settings
import hashlib
import glob
import os

def checksum(file_path):
    """
    Computes the SHA256 checksum of a file.
    """
    BUF_SIZE = 65536    # chunk size
    checksum = hashlib.sha256()
    with open(file_path, 'rb') as fp:
        while True:
            chunk = fp.read(BUF_SIZE)
            if not chunk:
                break
            checksum.update(chunk)

    return checksum.hexdigest()


def import_dataset(apps, schema_editor):
    """
    Import images from the dataset into the database, preprocessing as needed.
    """
    # we can't import the Image model directly as it may be a newer
    # version than this migration expects, so we use the historical version.

    Image = apps.get_model("api", "Image")
    STATIC_ROOT = settings.STATIC_ROOT
    DATASET_ROOT = settings.DATASET_ROOT
    dataset_images = glob.glob(os.path.join(DATASET_ROOT, "*.png"))
    dataset_images = dataset_images[:100]   # cap to first 100 images

    # for each image file, create a database entry
    print("\n\tAdding to database the entries for {} images found...".format(len(dataset_images)))
    for img_path in dataset_images:
        imgID = checksum(img_path)
        extension = img_path.split('/')[-1].split('.')
        extension = extension[-1] if len(extension) > 1 else ""
        img_static_path = img_path.split(DATASET_ROOT)[1]
        print(img_static_path)
        img = Image(imgID=imgID, extension=extension, imgStaticPath=img_static_path)
        img.save()
