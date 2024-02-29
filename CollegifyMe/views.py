from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count

from user.models import User
from student.models import StudentProfile
from college.models import CollegeProfile
from post.models import Post


def homePage(request):
    user = request.user
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return render(request, "account/login.html")
    else:
        print(user.email)
        if user.role == 1:
            # user is student
            user_profile = StudentProfile.objects.get(user=user)
            # print(user_profile.profile_image.url)
        elif user.role == 2:
            # user is college
            user_profile = CollegeProfile.objects.get(get=user)

    # Retrieve all posts ordered by post_date in descending order
    # Annotate each post with the count of likes it has
    posts = Post.objects.annotate(like_count=Count("postlike")).order_by("-post_date")

    context = {
        "user": user,
        "user_profile": user_profile,
        "posts": posts,
    }
    return render(request, "index.html", context=context)
