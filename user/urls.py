from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView, name="loginView"),
    path("register/", views.RegisterView, name="registerView"),
    path("registerCollege/", views.RegisterCollegeView, name="registerCollegeView"),
    path("forgetPassword/", views.ForgetPassword, name="forgetPasswordView"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("logout/", views.LogoutView, name="logoutView"),
]
