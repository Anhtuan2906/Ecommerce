import numpy as np
from django.shortcuts import render
from store.models import Product, Prediction

def index(request):
    np.random.seed(2107)

    products = Product.objects.all()
    no_recommended_1 = np.random.randint(0, 2, len(products)) * np.random.randint(0, 20, len(products))
    no_recommended_2 = no_recommended_1.copy()

    recommended_products_1 = [list(e) for e in zip(products, no_recommended_1)]
    recommended_products_1.sort(key=lambda x: x[1], reverse=True)

    recommended_products_2 = [list(e) for e in zip(products, no_recommended_2)]
    recommended_products_2.sort(key=lambda x: x[1], reverse=True)

    min_no_recommended = 2
    n = len(recommended_products_2)
    for r in range(n - 1, -1, -1):
        if recommended_products_2[r][1] < min_no_recommended:
            while recommended_products_2[r][1] < min_no_recommended:
                l = np.random.randint(0, r)
                if recommended_products_2[l][1] > min_no_recommended:
                    recommended_products_2[l][1] -= 1
                    recommended_products_2[r][1] += 1

    recommended_products_2.sort(key=lambda x: x[1], reverse=True)

    context = {
        'recommended_products_1': filter(lambda x: x[1] > 0, recommended_products_1),
        'recommended_products_2': filter(lambda x: x[1] > 0, recommended_products_2)
    }

    # Save prediction results
    for product, _ in recommended_products_1:
        Prediction.objects.create(user=request.user, item_id=product.id, prediction_value=np.random.rand())

    return render(request, 'recommendations/index.html', context)
