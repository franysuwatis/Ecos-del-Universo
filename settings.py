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

# 💡 AGREGAMOS LOS MIDDLEWARES (Aquí es donde WhiteNoise hace su magia)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Servidor de archivos estáticos eficiente
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

# 💡 CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS (Corregida y optimizada)
STATIC_URL = '/static/'

# Esta es la carpeta donde tienes tus fotos actualmente en desarrollo
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Esta es la carpeta donde WhiteNoise/Render unificarán todo para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Opcional: Esto comprime tus imágenes y archivos para que carguen un 50% más rápido
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'