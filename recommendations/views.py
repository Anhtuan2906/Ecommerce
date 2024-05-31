import numpy as np
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from store.models import Product, Prediction, OriginalPrediction, Interaction
from recommendations.models import ProductFeaturesVector, UserFeaturesVector
from recommendations.reranking import optimize


@login_required
def index(request):
    if request.method == 'POST':
        k = int(request.POST.get('no_recomend_item', 10))
        epsilon = float(request.POST.get('max_exposure', 0.1))

        # Retrieve all user feature vectors
        # user_feature_vectors = UserFeaturesVector.objects.all()
        # if not user_feature_vectors.exists():
        #     return render(request, 'recommendations/index.html', {'error': 'No user feature vectors found'})

        # user_ids = [ufv.user_id.id for ufv in user_feature_vectors]
        # user_matrix = np.array([np.fromstring(ufv.feature_vector.strip('[]'), sep=',') for ufv in user_feature_vectors])

        # # Retrieve all product feature vectors
        # product_feature_vectors = ProductFeaturesVector.objects.all()
        # if not product_feature_vectors.exists():
        #     return render(request, 'recommendations/index.html', {'error': 'No product feature vectors found'})

        # product_ids = [pfv.product_id.id for pfv in product_feature_vectors]
        # product_matrix = np.array([np.fromstring(pfv.feature_vector.strip('[]'), sep=',') for pfv in product_feature_vectors])

        # # Debugging prints
        # print(f"User Matrix Shape: {user_matrix.shape}")
        # print(f"Product Matrix Shape: {product_matrix.shape}")

        # # Ensure the matrices can be multiplied
        # if user_matrix.shape[1] != product_matrix.shape[1]:
        #     raise ValueError("User and product feature vectors must have the same length")

        # # Multiply the user matrix by the product matrix
        # interaction_matrix = np.dot(user_matrix, product_matrix.T)
        # optimized_matrix = optimize(interaction_matrix, k=k, epsilon=epsilon)

        # # Debugging prints
        # print(f"Interaction Matrix Shape: {optimized_matrix.shape}")

        # # Dummy context for demonstration purposes
        # context = {
        #     'pro
        #     'user_ids': user_ids,
        #     'product_ids': product_ids,
        # }

        # # Save prediction results (example with dummy predictions)
        # Prediction.objects.all().delete()
        # for user_id, user_vector in zip(user_ids, optimized_matrix):
        #     for product_id, prediction_value in zip(product_ids, user_vector):
        #         if prediction_value == 1:
        #             Prediction.objects.create(user_id=user_id, item_id=product_id, prediction_value=prediction_value)
    else:
        pass

    context = {}
    return render(request, 'recommendations/index.html', context)


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
    return render(request, 'recommendations/interaction_history.html', context)
