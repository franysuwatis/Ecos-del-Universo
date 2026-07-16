from django.urls import path
import views # Importamos tus funciones de views.py

urlpatterns = [
    # Cuando la dirección esté vacía (''), llama a la función sonificar_astro
    path('', views.sonificar_astro, name='index'),
]