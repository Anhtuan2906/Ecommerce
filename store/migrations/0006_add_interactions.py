import os
import json
from django.db import migrations

from ecommerce.settings import MEDIA_ROOT


def load_interactions(apps, schema_editor):
    Interaction = apps.get_model("store", "Interaction")
    User = apps.get_model("auth", "User")
    Product = apps.get_model("store", "Product")

    with open(MEDIA_ROOT + os.sep + "sample_interactions.json") as file:
        data = json.load(file)
        for interaction in data:
            user = User.objects.get(id=interaction["user_id"] + 1)
            product = Product.objects.get(id=interaction["product_id"] + 1)
            Interaction.objects.create(user=user, product=product)


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0003_remove_prediction_item_id_prediction_product_and_more"),
    ]

    operations = [
        migrations.RunPython(load_interactions),
    ]
