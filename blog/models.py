from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30)
    posted = models.BooleanField(default=False)
    time = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.title