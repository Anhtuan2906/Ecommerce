from django.shortcuts import render, redirect

from ecommerce.utils import require_login
from .models import *
from .forms import ProductForm


@require_login
def products(request):
    products = Product.objects.all()
    number_of_interactions = [Interaction.objects.filter(product=product).count() for product in products]

    context = {'products': list(zip(products, number_of_interactions))}
    return render(request, 'store/products.html', context)


@require_login
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)

    Interaction.objects.get_or_create(product=product, user=request.user)
    number_of_interactions = Interaction.objects.filter(product=product).count()

    context = {'product': product, 'number_of_interactions': number_of_interactions}

    return render(request, 'store/product_detail.html', context)


@require_login
def add_product(request):
    if request.method == 'GET':
        return render(request, 'store/add_product.html', {'form': ProductForm()})

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, 'store/add_product.html', {'form': ProductForm(), 'message': 'Product added successfully', 'is_error': False})
        else:
            return render(request, 'store/add_product.html', {'form': form, 'message': form.errors, 'is_error': True})

    return redirect('store:products')
