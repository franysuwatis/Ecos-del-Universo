import os
import sys
from django.core.wsgi import get_wsgi_application

# 1. Le decimos a Django dónde está la configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# 2. Creamos la variable "application" que buscará Render/Gunicorn
application = get_wsgi_application()

def main():
    # Esto le dice a Python dónde están las configuraciones de tu sitio
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()