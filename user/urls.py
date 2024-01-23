from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView, name="loginView"),
    path("register/", views.RegisterView, name="registerView"),
    path("forgetPassword/", views.ForgetPassword, name="forgetPasswordView"),
]
