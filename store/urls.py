from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('interaction_history/', views.interaction_history, name='interaction_history'),
]
