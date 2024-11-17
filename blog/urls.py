from .views import BlogView, render_home, create_blog
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'blog', BlogView, basename='blog')

urlpatterns = [
    path('api/', include(router.urls)),
    path('blog/', render_home, name='list-blog'),
    path('blog/create/', create_blog, name='create-blog')
]