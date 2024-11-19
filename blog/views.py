import requests
from django.shortcuts import render, redirect
from .models import Blog
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import BlogSerializer
from .forms import BlogForm
from dotenv import load_dotenv
import os

load_dotenv()

# Obtén la variable de entorno DEBUG y configura el BASE_URL
ENVIRONMENT = os.getenv('DEBUG', 'True').lower() == 'true'
BASE_URL = "https://railway-django-production-e532.up.railway.app" if not ENVIRONMENT else "http://localhost:8000"
API_ENDPOINT = "/api/blog/"

class BlogView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)

# Vista para renderizar el HTML
def render_home(request):
    print(requests.get(BASE_URL + API_ENDPOINT).json())
    try:
        api_url = f'{BASE_URL}{API_ENDPOINT}'  # Construye la URL completa
        # Realiza la solicitud GET y verifica el estado
        headers = {'Accept': 'application/json'}
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # Verificar si la respuesta fue exitosa (código 200)
        if response.status_code != 200:
            return render(request, 'error.html', {'message': f'Error al obtener blogs. Código: {response.status_code}'})
        data = response.json()
        # Intenta obtener los datos JSON
        print(response)
        return render(request, 'blog.html', {'blogs': data})  # Pasa los datos a la plantilla
    except requests.exceptions.RequestException as e:
        # Manejo de errores en solicitudes
        return render(request, 'error.html', {'message': f'Error al obtener blogs: {e}'})
    except ValueError:
        # Error si no se puede parsear JSON
        return render(request, 'error.html', {'message': 'Error al procesar la respuesta del servidor.'})

# Vista para crear un blog
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-blog')  # Cambia 'list-blog' según el nombre de tu URL
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})
