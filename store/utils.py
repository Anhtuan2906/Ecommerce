import os
import numpy as np
from sentence_transformers import SentenceTransformer


def get_image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{instance}.{ext}"
    return "products" + os.sep + f"{filename}"


def extract_product_feature(product):
    print("loading text model...")
    text_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')
    category_mapper = np.load(os.path.join("media", "categories_id.npy"), allow_pickle=True).item()

    categories = []
    categories_id = []
    for category in product.categories.all():
        categories.append(category.name)
        categories_id.append(category_mapper[category.name])

    context = product.name + " " + " ".join(categories) + " " + product.description + str(product.price)
    print(context)

    text_feature = text_model.encode(context)
    one_hot = np.zeros(len(category_mapper))
    one_hot[categories_id] = 1

    features = np.concatenate((text_feature, one_hot))
    features_128 = np.zeros(128)
    for i in range(128):
        features_128[i] = np.mean(features[i:i+len(features)-128])
    return features_128
