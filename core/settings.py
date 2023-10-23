"""
Django settings for lottolab project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import yaml
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ds-2$3co(domis5^eqg!awn(b7qw5tlon2!eknigb(m!n3)xa$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['192.168.0.9', 'tu_otra_direccion_ip', 'tu_nombre_de_host', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap4',
    "core",
    "lottoluck",
    'crispy_forms',
    'report',
    "django_unicorn",  # required for Django to register urls and templatetags




]
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'core.urls'

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
                'lottoluck.context_processor.total_compra',
                'lottoluck.context_processor.total_qty',
                'lottoluck.context_processor.total_linea',
                'lottoluck.context_processor.factura_secuencia',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

# Esto debe estar configurado con el nombre de tu URL de inicio de sesión si lo tienes.
LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'lottoluck_home'

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Cargar configuraciones desde el archivo YAML
# Obtener la ruta del archivo config.yaml
config_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'config.yaml')

# Cargar configuraciones desde el archivo YAML
with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Servidor SMTP de Gmail
EMAIL_PORT = 587  # Puerto TLS para Gmail
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False  # Deja esto en False
EMAIL_HOST_USER = config['correo']['email_address']
EMAIL_HOST_PASSWORD = config['correo']['email_password']
DEFAULT_FROM_EMAIL = config['correo']['email_address']
SERVER_EMAIL = config['correo']['email_password']

TWILIO_ACCOUNT_SID = config['twilio']['twilio_account_sid']
TWILIO_AUTH_TOKEN = config['twilio']['twilio_auth_token']
TWILIO_PHONE_NUMBER = config['twilio']['twilio_phone_number']

# Configura tus credenciales
NEXMO_API_KEY = 'gbZA3UsvERXAEg1J'
NEXMO_API_SECRET = 'xwdttbPrYZUDSfulTvOZOtLD6HaBBQ0i5lpn9iuEpReMZ0wmUct'

STATIC_URL = '/static/'

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'static')
#]
STATICFILES_DIRS = [
   BASE_DIR / 'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
