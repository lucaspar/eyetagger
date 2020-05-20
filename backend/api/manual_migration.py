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

from django.db import transaction, IntegrityError
from django.db import migrations, models
from django.conf import settings
import pandas as pd
import hashlib
import glob
import os


MAX_REGISTERED_IMAGES = -1


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

    # get list of images
    Image = apps.get_model("api", "Image")
    STATIC_ROOT = settings.STATIC_ROOT
    DATASET_ROOT = settings.DATASET_ROOT
    dataset_images = glob.glob(os.path.join(DATASET_ROOT, "*.png"))
    dataset_images = dataset_images[:MAX_REGISTERED_IMAGES]

    # load CSV dataframe
    df = pd.read_csv(os.path.join(DATASET_ROOT, "../metadata.csv"))
    FILENAME = 'filename'
    df = df.set_index(FILENAME)
    df.sort_values(by=[FILENAME])

    # for each image file, create a database entry
    cnt_not_found, cnt_created, cnt_duplicated = 0, 0, 0
    print("\n\tAdding to database the entries for {} images found...".format(len(dataset_images)))
    for img_ds_path in dataset_images:

        img_id      = checksum(img_ds_path)
        extension   = img_ds_path.split('/')[-1].split('.')
        extension   = extension[-1] if len(extension) > 1 else ""
        img_path    = (img_ds_path.split(DATASET_ROOT)[1]).strip(os.path.sep)

        # there might be duplicated files in the dataset
        # if image is already registered, skip it
        if Image.objects.filter(img_id=img_id).exists():
            print("Skipping duplicated element:\n\t{}\tSHA256: {}".format(
                img_path, img_id))
            cnt_duplicated += 1
            continue

        # matchings of CSV and DB fields
        db_fields   = ['user_id', 'sample_id', 'eye', 'lens_type', 'nir_illumination', 'lens_brand', 'is_regular']
        csv_fields  = ['user_id', 'sample_id', 'eye', 'live_fake', 'NIR_illumination', 'lens_brand', 'regular_irregular_lens_type']

        # extract file name from image path
        filename = os.path.basename(img_path).split('.')[0]
        snap = None
        try:
            snap = df.loc[filename]
            if snap.shape[0] > len(csv_fields):
                print("Discarding {} entries: filename must be unique!".format(snap.shape[0]))
                continue
        except:
            cnt_not_found += 1
            print("Skipping CSV filename not found: {}".format(filename))
            continue

        # map old csv values to new database ones
        mappings = {
            'live_fake': {
                'live':     'L',
                'fake':     'F',
                'clear':    'C',
            },
            'eye': {
                'left':     'L',
                'right':    'R',
            },
            'NIR_illumination': {
                'cross':    'C',
                'direct':   'D',
            },
            'regular_irregular_lens_type': {
                'regular':      True,
                'irregular':    False,
                'none':         None,
                'clear':        None,
            }
        }

        # map values and create image instance
        image_fields = dict()
        for db, csv in zip(db_fields, csv_fields):
            value = None
            try:
                value = snap.loc[csv]
            except:
                print(snap.head())
                raise Exception()
            if csv in mappings:     # translate value
                value = mappings[csv][value]
            image_fields.update({ db: value })

        # create instance
        img = Image(
            img_id      = img_id,
            extension   = extension,
            img_path    = img_path,
            **image_fields,
        )

        # execute transaction
        try:
            with transaction.atomic():
                img.save()
                cnt_created += 1
        except IntegrityError as err:
            print(" >> Failed to load entry from CSV into DB:")
            print(image_fields)
            raise err

    print("\n >> Duplicated entries:  {}".format(cnt_duplicated))
    print(" >> Entries not found:   {}".format(cnt_not_found))
    print(" >> Entries added:       {}".format(cnt_created))
