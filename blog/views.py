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

# Determina el entorno
ENVIRONMENT = os.getenv('DEBUG', 'True').lower() == 'true'

# Configura BASE_URL basado en el entorno
BASE_URL = "https://railway-django-production-e532.up.railway.app"
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
    try:
        api_url = f'{BASE_URL}{API_ENDPOINT}'  # Construye la URL completa
        
        response = requests.get(api_url)  # Establece un tiempo de espera
        data = response.json()  # Obtén los datos JSON
        return render(request, 'blog.html', {'blogs': data})  # Pasa los datos a la plantilla
    except requests.exceptions.RequestException as e:
        # Manejo de errores en solicitudes
        return render(request, 'error.html', {'message': f'Error al obtener blogs: {e}'})

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
