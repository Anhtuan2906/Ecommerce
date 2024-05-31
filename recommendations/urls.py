from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.index, name='index'),
    path('interaction_history/', views.interaction_history, name='interaction_history'),
]
