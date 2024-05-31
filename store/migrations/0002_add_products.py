import os
import json
import requests
import numpy as np
from io import BytesIO
from PIL import Image
from django.db import migrations

from ecommerce.settings import MEDIA_ROOT


def load_products_data(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    Category = apps.get_model("store", "Category")
    with open(MEDIA_ROOT + os.sep + "sample_products.json") as file:
        data = json.load(file)
        for idx, product in enumerate(data):
            img_path = os.path.join(MEDIA_ROOT,"products","{}.jpg".format(
                "product_" + str(idx) 
            ))
            img_data = requests.get(product["image"]).content
            img = Image.open(BytesIO(img_data))
            resized_img = img.resize((200, 200))
            resized_img.save(img_path)

            product_db = Product.objects.create(
                name=product["title"][:195] + "_" + str(idx),
                price=round(product["price"], 2),
                description=product["description"][:1000],
                image=img_path.replace(MEDIA_ROOT + os.sep, ""),
            )
            for category in product["categories"]:
                product_db.categories.add(Category.objects.get(name=category))
            product_db.save()


def load_categories_data(apps, schema_editor):
    Category = apps.get_model("store", "Category")
    categories_id = np.load(os.path.join(MEDIA_ROOT, "categories_id.npy"), allow_pickle=True).item()
    categories_id_sorted = {k: v for k, v in sorted(categories_id.items(), key=lambda item: item[1])}
    for category in categories_id_sorted.keys():
        Category.objects.create(name=category)


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0005_alter_product_categories"),
    ]

    operations = [
        migrations.RunPython(load_categories_data),
        migrations.RunPython(load_products_data),
    ]
