from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)  # <- новое поле

    def __str__(self):
        return self.title
