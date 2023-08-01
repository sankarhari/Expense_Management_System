from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add-expanse/', views.add_expense),
]
