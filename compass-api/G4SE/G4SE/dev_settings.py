"""
Django settings for G4SE project.

Generated by 'django-admin startproject' using Django 1.10b1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
if os.environ.get('SECRET_KEY', None) is None:
    os.environ['SECRET_KEY'] = 'dev_secret_key'
if os.environ.get('DATABASE_URL', None) is None:
    os.environ['DATABASE_URL'] = 'postgres://postgres:postgres@localhost:5432/G4SE'
if os.environ.get('ELASTIC_SEARCH_URL', None) is None:
    os.environ['ELASTIC_SEARCH_URL'] = 'http://localhost:9200/'

from .settings import *  # noqa
DEBUG = True
INTERNAL_IP_RANGES = ["127.0.0.1", '172.0.0.0/8']
INSTALLED_APPS.append('django_extensions')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('api.patch_debug_middleware.AdopdedTo110DebugMiddleware')
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda x: True
    }
