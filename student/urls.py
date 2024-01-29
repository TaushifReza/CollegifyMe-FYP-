from django.urls import path

from . import views

urlpatterns = [
    path(
        "studentRegistration/",
        views.StudentRegistrationView,
        name="studentRegistrationView",
    ),
]
