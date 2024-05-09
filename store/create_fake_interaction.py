import json
from random import randint
from django.contrib.auth.models import User
from store.models import Product, Interaction

def create_fake_interactions(num_interactions):
    # Load data from JSON files
    with open('C:\\Users\\ASUS\\Downloads\\Ecommerce\\media\\sample_users.json') as f:
        users_data = json.load(f)

    with open('C:\\Users\\ASUS\\Downloads\\Ecommerce\\media\\sample_products.json') as f:
        products_data = json.load(f)

    # Loop through the desired number of interactions
    for _ in range(num_interactions):
        # Choose a random user and product for the interaction
        random_user = User.objects.get(id=randint(1, len(users_data)))
        random_product = Product.objects.get(id=randint(1, len(products_data)))

        # Create the interaction and save it to the database
        interaction = Interaction(user=random_user, product=random_product)
        interaction.save()

# Adjust the number of interactions as needed
num_interactions = 100
create_fake_interactions(num_interactions)
