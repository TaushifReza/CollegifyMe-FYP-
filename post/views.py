from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

import time

from post.models import Post, PostMedia, PostLike


def PostCreationView(request):
    if request.method == "POST":
        # print("Hit")
        # time.sleep(3)
        # return redirect("homePage")
        current_user = request.user

        post_content = request.POST.get("post-content")
        post_media = request.FILES.getlist("post-media")

        print("POST Creation View HIT")
        print(post_content)
        try:
            post = Post(user=current_user, post_content=post_content)
            post.save()

            if post_media:  # Check if post_media has any files
                for each in post_media:
                    post_media = PostMedia(post=post, media_file=each)
                    post_media.save()
        except Exception as e:
            print(f"Error creating post: {e}")

        print("POST Creation View END")

        return redirect("homePage")


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
    # # return HttpResponse(pk)
    # if pk is None:
    #     return redirect("homePage")

    # current_user = request.user
    # post = get_object_or_404(Post, pk=pk)  # Fetch the Post instance

    # # Check if the user has already liked the post
    # already_liked = PostLike.objects.filter(post=post, user=current_user).exists()

    # if already_liked:
    #     # If the user has already liked the post, unlike it
    #     PostLike.objects.filter(post=post, user=current_user).delete()
    #     return redirect("homePage")
    # else:
    #     # If the user has not already liked the post, create a new like
    #     like_post = PostLike.objects.create(post=post, user=current_user)

    # return redirect("homePage")
