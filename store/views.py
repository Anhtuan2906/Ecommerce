import json
from django.shortcuts import render, redirect
from .models import Product, Interaction, Prediction
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

@login_required
def products(request):
    products = Product.objects.all()
    number_of_interactions = [Interaction.objects.filter(product=product).count() for product in products]
    context = {'products': list(zip(products, number_of_interactions))}
    return render(request, 'store/products.html', context)

@login_required
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.save_prediction(user=request.user, item_id=product_id, prediction_value=0.8)
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
            product.save_prediction(user=request.user, item_id=product.id, prediction_value=0.9)
            return render(request, 'store/add_product.html', {'form': ProductForm(), 'message': 'Product added successfully', 'is_error': False})
        else:
            return render(request, 'store/add_product.html', {'form': form, 'message': form.errors, 'is_error': True})
    return redirect('store:products')

@login_required
def interaction_history(request):
    user_interactions = Interaction.objects.filter(user=request.user)
    user_predictions = Prediction.objects.filter(user=request.user)
    recommended_products = [(pred.item_id, pred.prediction_value) for pred in user_predictions]
    
    context = {
        'user_interactions': user_interactions,
        'user_predictions': user_predictions,
        'recommended_products': recommended_products
    }
    return render(request, 'store/interaction_history.html', context)
