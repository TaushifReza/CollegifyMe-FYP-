from django.shortcuts import render, redirect

from post.models import Post, PostMedia


def PostCreationView(request):
    if request.method == "POST":
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
