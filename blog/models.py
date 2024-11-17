from django.db import models
from django.utils import timezone

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30)
    posted = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title