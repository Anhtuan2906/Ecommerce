import numpy as np
from django.shortcuts import render

from store.models import Product, Interaction, User

# Create your views here.
def index(request):
    products = Product.objects.all()
    no_recommended_1 = np.random.randint(0, 2, len(products)) * np.random.randint(0, 20, len(products))
    no_recommended_2 = np.random.randint(0, 2, len(products)) * np.random.randint(0, 20, len(products))

    recommended_products_1 = list(filter(lambda x: x[1] > 0, list(zip(products, no_recommended_1))))
    recommended_products_1.sort(key=lambda x: x[1], reverse=True)
    recommended_products_2 = list(filter(lambda x: x[1] > 0, list(zip(products, no_recommended_2))))
    recommended_products_2.sort(key=lambda x: x[1], reverse=True)

    context = {
        'recommended_products_1': recommended_products_1,
        'recommended_products_2': recommended_products_2
    }

    return render(request, 'recommendations/index.html', context)
