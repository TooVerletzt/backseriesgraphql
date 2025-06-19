import os
from pathlib import Path
import dj_database_url
import graphene_file_upload.scalars

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'replace-this-for-production')
DEBUG = True
ALLOWED_HOSTS = ['*']
APPEND_SLASH = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',

    # GraphQL + file upload
    'graphene_django',
    'graphql_jwt.refresh_token',       # si usas refresh tokens
    'graphene_file_upload.django',

    # Tu app
    'posts',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gameforum_api.urls'

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

WSGI_APPLICATION = 'gameforum_api.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
       # default='postgresql://postgres:123456@localhost:5432/vg_forum',
       default='postgres://avnadmin:AVNS_vHwXVeW9oxFLHOVYHWz@pg-22490183-estudiantes-8f4f.h.aivencloud.com:27787/seriesflix?sslmode=require',
        conn_max_age=600
    )
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'defaultdb',
#         'USER': 'avnadmin',
#         'PASSWORD': 'AVNS_vHwXVeW9oxFLHOVYHWz',
#         'HOST': 'pg-22490183-estudiantes-8f4f.h.aivencloud.com',
#         'PORT': '27787',
#         'OPTIONS': {
#             'sslmode': 'require'
#         }
#     }
# }





AUTH_PASSWORD_VALIDATORS = [
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

STATIC_URL = '/static/'

# Media (para servir imágenes)
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Graphene + file upload
GRAPHENE = {
    'SCHEMA': 'posts.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
    'SCALARS': {
        'Upload': graphene_file_upload.scalars.Upload,
    }
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

CORS_ORIGIN_ALLOW_ALL = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
