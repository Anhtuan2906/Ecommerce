def get_image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{instance}.{ext}"
    return f"products/{filename}"
