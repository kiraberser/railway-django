from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics

from .models import Blog
from .serializers import BlogSerializer

# Create your views here.

class BlogView(generics.GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer 

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)
    def render_home(self, request):
        return render(request, 'blog.html')

blog_view = BlogView.as_view()