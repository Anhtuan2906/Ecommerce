import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProductForm
from .utils import extract_product_feature
from .models import Product, Interaction, Prediction
from recommendations.models import ProductFeaturesVector


@login_required
def products(request):
    products = Product.objects.all()
    number_of_interactions = [Interaction.objects.filter(product=product).count() for product in products]
    context = {'products': list(zip(products, number_of_interactions))}
    return render(request, 'store/products.html', context)

@login_required
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    Interaction.objects.get_or_create(product=product, user=request.user)
    number_of_interactions = Interaction.objects.filter(product=product).count()
    context = {'product': product, 'number_of_interactions': number_of_interactions}
    return render(request, 'store/product_detail.html', context)

@login_required
def add_product(request):
    if request.method == 'GET':
        with open('media/categories.json') as f:
            categories = json.load(f)
        return render(request, 'store/add_product.html', {'form': ProductForm(), 'categories': categories})
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            product_feature = extract_product_feature(product)

            product_feature = json.dumps(product_feature.tolist())
            ProductFeaturesVector.objects.create(product_id=product, feature_vector=product_feature)
            return render(request, 'store/add_product.html', {'form': ProductForm(), 'message': 'Product added successfully', 'is_error': False})
        else:
            return render(request, 'store/add_product.html', {'form': form, 'message': form.errors, 'is_error': True})
    return redirect('store:products')
