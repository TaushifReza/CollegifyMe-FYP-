from django.urls import path

from post import views

urlpatterns = [
    path("create_post/", views.PostCreationView, name="postCreationView"),
    path("like_post/<int:pk>/", views.LikePostView, name="likePostView"),
    path("comment_post/<int:pk>/", views.CommentPostView, name="commentPostView"),
]
