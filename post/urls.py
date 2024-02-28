from django.urls import path

from post import views

urlpatterns = [
    path("create_post/", views.PostCreationView, name="postCreationView"),
]
