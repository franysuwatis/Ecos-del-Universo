from django.shortcuts import render
from alerce.core import Alerce
from alerce.exceptions import ObjectNotFoundError
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def generar_secuencia_sonora(datos_alerce):
    # 1. Extraemos las magnitudes como un arreglo de numpy
    magnitudes = datos_alerce['magpsf'].to_numpy()
    
    # 2. Definimos las constantes de la fórmula recomendada
    D_max = -6.0      # Volumen máximo en dBFS
    D_min = -30.0     # Volumen mínimo audible en dBFS
    
    # Usamos el percentil 5 como referencia para ignorar datos basura erróneos
    m_ref = np.percentile(magnitudes, 5) 
    
    # 3. Aplicamos la ecuación: D_i = D_max - 4 * (m_i - m_ref)
    volumenes_db = D_max - 4 * (magnitudes - m_ref)
    
    # 4. Aplicamos el 'clip' para mantener el volumen entre -30 y -6 dBFS
    volumenes_acotados = np.clip(volumenes_db, D_min, D_max)
    
    # Convertimos el resultado a una lista de Python para mandarla a tu index.html
    return volumenes_acotados.tolist()

def sonificar_astro(request):
    contexto = {'error_busqueda': False}
    
    if request.method == 'POST':
        try:
            oid = request.POST.get('oid_busqueda')
            client = Alerce()
        
            # Buscamos las detecciones en ALerCE
            detecciones = client.query_detections(oid, format="pandas")
            
            # Ordenamos las detecciones por fecha (MJD) para que suenen cronológicamente
            detecciones = detecciones.sort_values(by='mjd')
            
            # Generamos los volúmenes en decibelios usando la nueva fórmula
            lista_de_volumenes = generar_secuencia_sonora(detecciones)
            
            # Creamos una lista de diccionarios con las tres variables unidas por cada punto
            puntos_curva = []
            mjds = detecciones['mjd'].tolist()
            magnitudes = detecciones['magpsf'].tolist()
            
            for i in range(len(mjds)):
                puntos_curva.append({
                    'mjd': mjds[i],
                    'magnitud': magnitudes[i],
                    'volumen': lista_de_volumenes[i]
                })
        
            # Creamos el gráfico de la curva de luz
            # --- Modificación en views.py ---
            plt.figure(figsize=(8, 4))
            plt.plot(detecciones['mjd'], detecciones['magpsf'], 'bo')

            # Añadimos las etiquetas a los ejes:
            plt.xlabel("Tiempo (MJD)")       # <-- Nombre para el eje X
            plt.ylabel("Brillo (Magnitud)")  # <-- Nombre para el eje Y
            plt.grid(True, linestyle='--', alpha=0.5)

            plt.title(f"Curva de Luz de {oid}")
            plt.gca().invert_yaxis() 
        
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            grafico_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
        
            contexto = {
                'grafico': grafico_base64,
                'puntos': puntos_curva,           # <-- Pasamos toda la data empaquetada
                'frecuencias': lista_de_volumenes, # <-- Mantenemos esto para que el JS lea los volúmenes directo
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