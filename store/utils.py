import os
import numpy as np
from sentence_transformers import SentenceTransformer


def get_image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{instance}.{ext}"
    return "products" + os.sep + f"{filename}"


def extract_product_feature(product):
    print("loading text model...")
    text_model = SentenceTransformer(os.environ.get("TEXT_MODEL_NAME"))
    category_mapper = np.load(os.path.join("media", "categories_id.npy"), allow_pickle=True).item()

    categories = []
    categories_id = []
    for category in product.categories.all():
        categories.append(category_mapper[category.name])
        categories_id.append(category_mapper[category.name])

    context = product.name + " " + " ".join(categories) + " " + product.description + product.price

    text_feature = text_model.encode(context)
    one_hot = np.zeros(len(category_mapper))
    one_hot[categories_id] = 1

    features = np.cat([text_feature, one_hot])

    return features
