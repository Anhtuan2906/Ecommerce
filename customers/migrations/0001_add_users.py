import os 
import json
from django.db import migrations

from ecommerce.settings import MEDIA_ROOT

def load_users_data(apps, schema_editor):
    User = apps.get_model("auth", "User")
    with open(MEDIA_ROOT + os.sep + "sample_users.json") as file:
        data = json.load(file)
        for user in data:
            User.objects.create_user(
                username=user["username"],
                email=user["email"],
                password=user["password"],
                is_staff=user["is_staff"],
                is_superuser=user["is_superuser"],
            )

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_users_data),
    ]
