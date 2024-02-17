from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser

from user.models import User
from student.models import StudentProfile
from college.models import CollegeProfile


def homePage(request):
    print("HIT")
    user = request.user
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        print("Not Login")
        return render(request, "account/login.html")
    else:
        print("Login")
        print(user.email)
        if user.role == 1:
            # user is student
            print("Student")
            print(user.role)
            user_profile = StudentProfile.objects.get(user=user)
            print(user_profile.profile_image.url)
        elif user.role == 2:
            # user is college
            print("College")
            print(user.role)
            user_profile = CollegeProfile.objects.get(get=user)

    context = {"user": user, "user_profile": user_profile}
    return render(request, "index.html", context=context)
