import os
import json
import requests
from io import BytesIO
from PIL import Image
from django.db import migrations

from ecommerce.settings import MEDIA_ROOT


def load_products_data(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    with open(MEDIA_ROOT + os.sep + "sample_products.json") as file:
        data = json.load(file)
        for product in data:
            img_path = os.path.join(MEDIA_ROOT,"products","{}.jpg".format(
                product["title"].title().replace("/", "").replace("\\", "").replace(" ", "_")
            ))
            img_data = requests.get(product["image"]).content
            img = Image.open(BytesIO(img_data))
            resized_img = img.resize((200, 200))
            resized_img.save(img_path)

            Product.objects.create(
                name=product["title"],
                category=product["category"],
                price=round(product["price"], 2),
                description=product["description"],
                image=img_path.replace(MEDIA_ROOT + os.sep, ""),
            )


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_products_data),
    ]
