from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class ProductFeaturesVector(models.Model):
    product_id = models.OneToOneField(Product, on_delete=models.CASCADE)
    feature_vector = models.TextField()

    def __str__(self):
        return f"Feature vector for product {self.product_id}"

class UserFeaturesVector(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    feature_vector = models.TextField()

    def __str__(self):
        return f"Feature vector for user {self.user_id}"
