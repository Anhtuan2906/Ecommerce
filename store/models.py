from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

from .utils import get_image_path

class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    category = models.CharField(max_length=200, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    image = ResizedImageField(size=[200, 200], quality=100, upload_to=get_image_path, null=False, blank=False, default='no_image.jpeg')

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Interaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')
        indexes = [
            models.Index(fields=['product', 'user']),
        ]
