from django.urls import path

from . import views

urlpatterns = [
    path(
        "collegeRegistration/",
        views.CollegeRegistrationView,
        name="collegeRegistrationView",
    ),
]
