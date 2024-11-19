from rest_framework.pagination import PageNumberPagination
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

class BlogPagination(PageNumberPagination):
    page_size = 10
class BlogView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)

# Vista para renderizar el HTML
from .serializers import BlogSerializer

def render_home(request):
    queryset = Blog.objects.all()
    serializer = BlogSerializer(queryset, many=True)
    return render(request, 'blog.html', {'blogs': serializer.data})


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
