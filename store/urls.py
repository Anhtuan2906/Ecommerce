from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('update_click_count/', views.update_click_count, name='update_click_count'),
    path('update_star_rating/', views.update_star_rating, name='update_star_rating'),
]
