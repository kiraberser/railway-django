import requests
from django.shortcuts import render, redirect
from .models import Blog
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import BlogSerializer
from .forms import BlogForm

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
        # Obtén todos los blogs de la base de datos
        blogs = Blog.objects.all()

        # Usa el serializer para serializar los datos
        serializer = BlogSerializer(blogs, many=True)

        # Renderiza la plantilla pasando los datos serializados
        return render(request, 'blog.html', {'blogs': serializer.data})

    except Exception as e:
        # Manejo de errores
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
