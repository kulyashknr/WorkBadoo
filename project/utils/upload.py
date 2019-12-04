import os
import shutil
from datetime import datetime


def user_photo_path(instance, filename):
    return f'photos/{filename}'


def photo_delete_path(document):
    datetime_path = os.path.abspath(os.path.join(document.path, '..'))
    shutil.rmtree(datetime_path)