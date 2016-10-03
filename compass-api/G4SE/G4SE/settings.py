"""
Django settings for G4SE project.

Generated by 'django-admin startproject' using Django 1.10b1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

import environ

env = environ.Env(DEBUG=(bool, False),)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Internal IP ranges for displaying internal data
# Not out of the Env, so they can easily be modified in production
INTERNAL_IP_RANGES = ["152.96.0.0/16", "152.96.244.0/23"]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_swagger',

    'haystack',

    'corsheaders',
    'rest_framework',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Static Assets
# ------------------------
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'G4SE.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'G4SE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db(),
}
# DATABASES['default']['OPTIONS'] = {'options': '-c search_path=django,public'}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_ROOT = env.str('STATIC_ROOT', default=os.path.abspath(os.path.join(BASE_DIR, '..', 'static')))
STATIC_URL = env.str('STATIC_URL', '/api/static/')

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
DEBUG_TOOLBAR_PATCH_SETTINGS = False

# HAYSTACK CONFIGURATION
DEFAULT_INDEX_SETUP = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["haystack_ngram", "lowercase"]
                    },
                    "edgengram_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["haystack_edgengram", "lowercase"]
                    },
                },
                "tokenizer": {
                    "haystack_ngram_tokenizer": {
                        "type": "nGram",
                        "min_gram": 3,
                        "max_gram": 15,
                    },
                    "haystack_edgengram_tokenizer": {
                        "type": "edgeNGram",
                        "min_gram": 2,
                        "max_gram": 15,
                        "side": "front"
                    }
                },
                "filter": {
                    "haystack_ngram": {
                        "type": "nGram",
                        "min_gram": 3,
                        "max_gram": 15
                    },
                    "haystack_edgengram": {
                        "type": "edgeNGram",
                        "min_gram": 2,
                        "max_gram": 15
                    },
                }
            }
        },
    },
}

GERMAN_INDEX_SETTINGS = DEFAULT_INDEX_SETUP.copy()
GERMAN_INDEX_SETTINGS["settings"]["index"]["analysis"]["analyzer"]["german_stemmer"] = {
    "tokenizer": "standard",
    "filter": ["standard", "lowercase", "german_stemmer"],
}
GERMAN_INDEX_SETTINGS["settings"]["index"]["analysis"]["filter"]["german_stemmer"] = {
    "type": "stemmer",
    "name": "german",
}
ENGLISH_INDEX_SETTINGS = DEFAULT_INDEX_SETUP.copy()
ENGLISH_INDEX_SETTINGS["settings"]["index"]["analysis"]["analyzer"]["english_stemmer"] = {
    "tokenizer": "standard",
    "filter": ["standard", "lowercase", "english_stemmer"],
}
ENGLISH_INDEX_SETTINGS["settings"]["index"]["analysis"]["filter"]["english_stemmer"] = {
    "type": "stemmer",
    "name": "english",
}
FRENCH_INDEX_SETTINGS = DEFAULT_INDEX_SETUP.copy()
FRENCH_INDEX_SETTINGS["settings"]["index"]["analysis"]["analyzer"]["french_stemmer"] = {
    "tokenizer": "standard",
    "filter": ["standard", "lowercase", "french_stemmer"],
}
FRENCH_INDEX_SETTINGS["settings"]["index"]["analysis"]["filter"]["french_stemmer"] = {
    "type": "stemmer",
    "name": "english",
}

HAYSTACK_CONNECTIONS = {
    # default is english!
    'default': {
        'ENGINE': 'configurable_elastic_search_backend.backends.ConfigurableElasticEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'haystack',
        'EXCLUDED_INDEXES': [
            'api.search_indexes.EnglishCombinedRecordIndex',
            'api.search_indexes.GermanCombinedRecordIndex',
            'api.search_indexes.FrenchCombinedRecordIndex',
        ],
    },
    'en': {
        'ENGINE': 'configurable_elastic_search_backend.backends.EnglishConfigurableElasticEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'haystack_english',
        'EXCLUDED_INDEXES': [
            'api.search_indexes.CombinedRecordIndex',
            'api.search_indexes.GermanCombinedRecordIndex',
            'api.search_indexes.FrenchCombinedRecordIndex',
        ],
        "OPTIONS": {
            **ENGLISH_INDEX_SETTINGS,
        },
    },
    'de': {
        'ENGINE': 'configurable_elastic_search_backend.backends.GermanConfigurableElasticEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'haystack_german',
        'EXCLUDED_INDEXES': [
            'api.search_indexes.CombinedRecordIndex',
            'api.search_indexes.EnglishCombinedRecordIndex',
            'api.search_indexes.FrenchCombinedRecordIndex',
        ],
        "OPTIONS": {
            **GERMAN_INDEX_SETTINGS,
        },
    },
    'fr': {
        'ENGINE': 'configurable_elastic_search_backend.backends.FrenchConfigurableElasticEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'haystack_french',
        'EXCLUDED_INDEXES': [
            'api.search_indexes.CombinedRecordIndex',
            'api.search_indexes.EnglishCombinedRecordIndex',
            'api.search_indexes.GermanCombinedRecordIndex',
        ],
        "OPTIONS": {
            **FRENCH_INDEX_SETTINGS,
        },
    },
}
HAYSTACK_DOCUMENT_FIELD = 'text'
HAYSTACK_SIGNAL_PROCESSOR = 'api.signals.CombinedRecordRealtimeSignalProcessor'
