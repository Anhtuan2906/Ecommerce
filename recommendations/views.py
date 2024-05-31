import numpy as np
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from store.models import Product, Prediction, OriginalPrediction, Interaction
from customers.models import User
from recommendations.models import ProductFeaturesVector, UserFeaturesVector
from recommendations.reranking import optimize, normalize, optimizeORTools, UMMFReRanking


def convert_preference_matrix_decision_matrix(S, top_k=10):
    S_idx = np.argsort(S, axis=1)
    B = np.zeros_like(S)
    for i in range(S.shape[0]):
        B[i, S_idx[i, -top_k:]] = 1
    return B


def convert_predictons_products_list(predictions):
    products = {}

    for prediction in predictions:
        product_id = prediction.product.id
        if product_id not in products:
            products[product_id] = 0
        products[product_id] += 1

    return [(Product.objects.get(id=product_id), count) for product_id, count in products.items()]


@login_required
def index(request):
    message = None
    is_error = False
    if request.method == 'POST':
        k = int(request.POST.get('k', 10))
        p = float(request.POST.get('p', 10)) / 100

        # Retrieve all user feature vectors
        user_feature_vectors = UserFeaturesVector.objects.all()
        if not user_feature_vectors.exists():
            return render(request, 'recommendations/index.html', {'error': 'No user feature vectors found'})

        user_ids = [ufv.user_id.id for ufv in user_feature_vectors]
        user_matrix = np.array([np.fromstring(ufv.feature_vector.strip('[]'), sep=',') for ufv in user_feature_vectors])


        # Retrieve all product feature vectors
        product_feature_vectors = ProductFeaturesVector.objects.all()
        if not product_feature_vectors.exists():
            return render(request, 'recommendations/index.html', {'error': 'No product feature vectors found'})

        product_ids = [pfv.product_id.id for pfv in product_feature_vectors]
        product_matrix = np.array([np.fromstring(pfv.feature_vector.strip('[]'), sep=',') for pfv in product_feature_vectors])


        # Debugging prints
        print(f"User Matrix Shape: {user_matrix.shape}")
        print(f"Product Matrix Shape: {product_matrix.shape}")


        # Ensure the matrices can be multiplied
        if user_matrix.shape[1] != product_matrix.shape[1]:
            raise ValueError("User and product feature vectors must have the same length")

        interaction_matrix = np.dot(user_matrix, product_matrix.T)
        interaction_matrix = normalize(interaction_matrix)
        print(interaction_matrix)

        # Save prediction results (original)
        decision_matrix = convert_preference_matrix_decision_matrix(interaction_matrix, top_k=k)
        OriginalPrediction.objects.all().delete()
        for user_id, user_vector in zip(user_ids, decision_matrix):
            for product_id, prediction_value in zip(product_ids, user_vector):
                if prediction_value == 1:
                    OriginalPrediction.objects.create(user=User.objects.get(id=user_id), product=Product.objects.get(id=product_id), prediction_value=prediction_value)


        # Save prediction results (reranking)
        if p > 0:
            last_hope = UMMFReRanking()
            try:
                reranked_decision_matrix = last_hope.optimize(interaction_matrix, k=k, p=p)
            except Exception as e:
                reranked_decision_matrix = decision_matrix
                is_error = True
                message = str(e)
            if np.sum(reranked_decision_matrix) == 0:
                reranked_decision_matrix = decision_matrix
                is_error = True
                message = "No solution"
        else:
            reranked_decision_matrix = decision_matrix
        Prediction.objects.all().delete()
        for user_id, user_vector in zip(user_ids, reranked_decision_matrix):
            for product_id, prediction_value in zip(product_ids, user_vector):
                if prediction_value == 1:
                    Prediction.objects.create(user=User.objects.get(id=user_id), product=Product.objects.get(id=product_id), prediction_value=prediction_value)

        # Debugging prints
        print(f"Interaction Matrix Shape: {interaction_matrix.shape}")
        print(f"Decision Matrix Shape: {decision_matrix.shape}")
        print(f"Reranked Decision Matrix Shape: {reranked_decision_matrix.shape}")

    context = {
        "is_error": is_error,
        "message": message,
        "recommended_products_1": convert_predictons_products_list(OriginalPrediction.objects.all()),
        "recommended_products_2": convert_predictons_products_list(Prediction.objects.all())
    }

    return render(request, 'recommendations/index.html', context)


@login_required
def interaction_history(request):
    user_interactions = Interaction.objects.filter(user=request.user)
    user_original_predictions = OriginalPrediction.objects.filter(user=request.user)
    user_predictions = Prediction.objects.filter(user=request.user)

    context = {
        "user_interactions": user_interactions,
        "recommended_products_1": convert_predictons_products_list(user_original_predictions),
        "recommended_products_2": convert_predictons_products_list(user_predictions)
    }

    return render(request, 'recommendations/interaction_history.html', context)
