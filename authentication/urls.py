from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("validate-username", views.username_validation, name="validate-username"),
    path("validate-email", views.email_validation, name="validate-email"),
    path("validate-password", views.password_validation, name = "validate-password")
]
