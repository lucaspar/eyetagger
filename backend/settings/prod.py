""" Production Settings """

import os
import dj_database_url
from .dev import *

############
# DATABASE #
############
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DB_HOST')
    )
}

############
# SECURITY #
############

# DEBUG = bool(os.getenv('DEBUG', ''))
# SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)

# Set to your Domain here (eg. 'django-vue-template-demo.herokuapp.com')
ALLOWED_HOSTS = ['*']
