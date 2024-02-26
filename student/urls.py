from django.urls import path

from . import views

urlpatterns = [
    path(
        "studentRegistration/",
        views.StudentRegistrationView,
        name="studentRegistrationView",
    ),
    path("studentProfileView/", views.StudentProfileView, name="studentProfileView"),
    path("friends/", views.AddFriendsView, name="addFriendsView"),
    path("addFriends/<int:pk>/", views.SendFriendRequestView, name="sendFriendRequest"),
    path(
        "acceptRequest/<int:pk>/",
        views.AcceptFriendRequest,
        name="acceptFriendRequest",
    ),
    path(
        "declineRequest/<int:pk>/",
        views.DeclineFriendRequest,
        name="declineFriendRequest",
    ),
]
