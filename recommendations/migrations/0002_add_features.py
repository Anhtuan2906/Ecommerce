import os
import json
import torch
import numpy as np
from django.conf import settings
from django.db import migrations, models

from django.contrib.auth.models import User


def load_features_vector(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    User = apps.get_model("auth", "User")
    ProductFeaturesVector = apps.get_model("recommendations", "ProductFeaturesVector")
    UserFeaturesVector = apps.get_model("recommendations", "UserFeaturesVector")

    embedding_matrix = torch.load(os.path.join("media", "clcrec.pt"), map_location=torch.device('cpu')) * 1e3
    print(embedding_matrix.shape)
    item_id_mapper = np.load(os.path.join("media", "item_id_mapper.npy"))
    user_id_mapper = np.load(os.path.join("media", "user_id_mapper.npy"))

    for i, product in enumerate(Product.objects.all()):
        ProductFeaturesVector.objects.create(
            product_id=product,
            feature_vector=json.dumps(embedding_matrix[item_id_mapper[product.id - 1] + 3714].tolist())
        )

    for i, user in enumerate(User.objects.all()):
        UserFeaturesVector.objects.create(
            user_id=user,
            feature_vector=json.dumps(embedding_matrix[user_id_mapper[user.id - 1]].tolist())
        )


class Migration(migrations.Migration):
    dependencies = [
        ('customers', '0001_add_users'),
        ('store', '0002_add_products'),
        ('recommendations', '0001_initial')
    ]

    operations = [
        migrations.RunPython(load_features_vector),
    ]
