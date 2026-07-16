from django.shortcuts import render
from alerce.core import Alerce
from alerce.exceptions import ObjectNotFoundError
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64

def generar_secuencia_sonora(datos_alerce):
    notas_musicales = [] 
    for brillo in datos_alerce['magpsf']:
        frecuencia = brillo * 100 + 440 
        notas_musicales.append(frecuencia) 
    return notas_musicales

def sonificar_astro(request):
    contexto = {'error_busqueda': False}
    
    if request.method == 'POST':
        try:
            oid = request.POST.get('oid_busqueda')
            client = Alerce()
        
        
            detecciones = client.query_detections(oid, format="pandas")
            
        
            lista_de_notas = generar_secuencia_sonora(detecciones)
        
        
            plt.figure(figsize=(8, 4))
            plt.plot(detecciones['mjd'], detecciones['magpsf'], 'bo')
            plt.title(f"Curva de Luz de {oid}")
            plt.gca().invert_yaxis() 
        
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            grafico_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
        
            contexto = {
                'grafico': grafico_base64,
                'frecuencias': lista_de_notas, 
                'oid': oid,
                'error_busqueda': False
            }

        except ObjectNotFoundError:
            contexto = {
                'error_busqueda': True,
                'mensaje_error': f"El ID '{oid}' no fue encontrado en la base de datos."
            }
        print("¡Ups! El ID no fue encontrado, pero el servidor sigue vivo. Prueba con otro término.")
    
    return render(request, 'index.html', contexto)