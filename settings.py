import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Configuración básica de seguridad (solo para desarrollo local)
SECRET_KEY = 'django-insecure-clave-de-prueba-para-desarrollo'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
]

# Configuración de URLs principales
ROOT_URLCONF = 'urls'

# Configuración del motor de plantillas (clave para que encuentre tu index.html)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]
STATIC_URL = 'static/'