from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(Interaction)
admin.site.register(Prediction)
admin.site.register(Category)
admin.site.register(OriginalPrediction)
