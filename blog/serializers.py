from rest_framework.serializers import ModelSerializer
from .models import Blog

class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'title',
            'content',
            'slug',
            'posted',
            'time'
        ]

