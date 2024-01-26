from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView, name="loginView"),
    path("register/", views.RegisterView, name="registerView"),
    path("forgetPassword/", views.ForgetPassword, name="forgetPasswordView"),
    path("registration/", views.RegistrationView, name="registrationView"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
