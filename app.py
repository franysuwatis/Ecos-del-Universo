import os
import sys
from django.core.wsgi import get_wsgi_application

# 1. Le decimos a Django dónde está la configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# 2. Creamos la variable "application" que buscará Render/Gunicorn
application = get_wsgi_application()

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado?"
        ) from exc
    
    # 💡 DETECTAMOS EL PUERTO DE RENDER
    # Si Render nos da un puerto, lo usamos. Si no (como en tu Mac), usamos el puerto 8000 por defecto.
    port = os.environ.get("PORT", "8000")
    
    # Si ejecutas "python app.py" sin argumentos extras (como pasa en Render):
    if len(sys.argv) == 1:
        # Le decimos a Django que levante el servidor automáticamente en el puerto correcto
        sys.argv = [sys.argv[0], "runserver", f"0.0.0.0:{port}"]
        
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()