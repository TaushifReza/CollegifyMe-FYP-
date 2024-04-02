from django.urls import path

from chat import views

urlpatterns = [
    path("chat/", views.messages_page, name="chat"),
]
