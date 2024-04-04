import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Case, Value, When, Count, F, Func

from cloudinary.models import CloudinaryField
import cloudinary

import time

from post.models import Post, PostMedia, PostLike, PostComment
from post.serializers import PostSerializer
from user.models import User


def PostCreationView(request):
    if (
        request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        and request.method == "POST"
    ):
        current_user = request.user
        post_content = request.POST.get("post-content")
        post_media = request.FILES.getlist("post-media")

        try:
            post = Post(user=current_user, post_content=post_content)
            post.save()

            if post_media:  # Check if post_media has any files
                for each in post_media:
                    post_media = PostMedia(post=post, media_file=each)
                    post_media.save()
        except Exception as e:
            return JsonResponse({"message": str(e), "status": "Failed"})

        return JsonResponse({"message": "Form posted", "status": "Success"})


def LikePostView(request, pk=None):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Please login to continued!!!", "status": "Failed"}
        )
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # check if post exists
        try:
            current_user = request.user
            post = Post.objects.get(pk=pk)

            # Check if the user has already liked the post
            already_liked = PostLike.objects.filter(
                post=post, user=current_user
            ).exists()

            if already_liked:
                # If the user has already liked the post, unlike it
                PostLike.objects.filter(post=post, user=current_user).delete()
                like_status = "DisLike Post"
                return JsonResponse({"message": "DisLike Post", "status": "Success"})
            else:
                # If the user has not already liked the post, create a new like
                like_post = PostLike.objects.create(post=post, user=current_user)
                like_status = "Like Post"

            # Get total number of likes for the post
            total_likes_count = PostLike.objects.filter(post=post).count()
            if total_likes_count > 0:
                print("Toatl Like: ", total_likes_count)
            elif total_likes_count is None:
                print("Toatl Like: None")

            return JsonResponse(
                {
                    "message": like_status,
                    "status": "Success",
                    "total_likes": total_likes_count,
                }
            )
        except:
            return JsonResponse(
                {"message": "This post does not exist!!!", "status": "Failed"}
            )
    else:
        return JsonResponse({"message": "Invalid Request!!!", "status": "Failed"})


def CommentPostView(request, pk=None):
    if (
        request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        and request.method == "POST"
    ):
        print("HIT CommentPostView")
        current_user = request.user
        post_pk = int(request.POST.get("post-pk"))
        comment_content = request.POST.get("comment-content")

        user_comment_exist = PostComment.objects.filter(
            post_id=post_pk, user_id=current_user.id
        )
        if user_comment_exist.exists():
            return JsonResponse(
                {
                    "message": "User have already comment in this post.",
                    "status": "Failed",
                }
            )
        # Save comment to db
        comment_post = PostComment.objects.create(
            post_id=post_pk, user_id=current_user.id, comment_content=comment_content
        )
        print(post_pk)
        print(comment_content)

        return JsonResponse({"message": "Commented", "status": "Success"})


def GetPostCommentsView(request, pk=None):
    if (
        request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        and request.method == "GET"
    ):
        print("HIT GetPostComments")
        current_user = request.user
        comments = (
            PostComment.objects.filter(post_id=pk)
            .select_related("user", "user__studentprofile", "user__collegeprofile")
            .annotate(
                profile_image_url=Case(
                    When(
                        user__role=User.STUDENT,
                        then=F("user__studentprofile__profile_image"),
                    ),
                    When(
                        user__role=User.COLLEGE,
                        then=F("user__collegeprofile__college_logo"),
                    ),
                    default=Value(None),
                ),
                user_full_name=Case(
                    When(
                        user__role=User.STUDENT,
                        then=Func(
                            F("user__studentprofile__first_name"),
                            Value(" "),
                            F("user__studentprofile__last_name"),
                            function="CONCAT",
                        ),
                    ),
                    When(
                        user__role=User.COLLEGE,
                        then=F("user__collegeprofile__college_name"),
                    ),
                    default=Value(None),
                ),
            )
            .values(
                "id",
                "comment_content",
                "user_id",
                "user__email",
                "user_full_name",
                "profile_image_url",
            )
        )
        comment_list = []
        for comment in comments:
            if comment["profile_image_url"]:
                comment["profile_image_url"] = comment["profile_image_url"].url
            comment_list.append(comment)
        # serializers_comment = PostSerializer(comments, many=True)
        print(comments)

        return JsonResponse({"comment_data": comment_list, "status": "Success"})
