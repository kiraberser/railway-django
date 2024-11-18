import requests
from django.shortcuts import render, redirect
from .models import Blog
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import BlogSerializer
from .forms import BlogForm
from dotenv import load_dotenv

load_dotenv()
# Vista para la API (correcta, no necesitas cambiarla)
ENVIRONMENT = False

BASE_URL = "http://localhost:8000" if ENVIRONMENT else "https://railway-django-production-e532.up.railway.app"
API_ENDPOINT = "/api/blog/"

class BlogView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer 

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)

# Vista para renderizar el HTML (corrige el uso de requests)
def render_home(request):
    api_url = f'{BASE_URL}{API_ENDPOINT}'  # Asegúrate de que la URL es correcta
    print(api_url)
    response = requests.get(api_url)

    if response.status_code != 200:
        return render(request, 'error.html', {'message': 'No se pudieron obtener los blogs'})

    data = response.json()  # Obtén los datos JSON
    return render(request, 'blog.html', {'blogs': data})  # Pasa los datos a la plantilla

def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-blog')
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})