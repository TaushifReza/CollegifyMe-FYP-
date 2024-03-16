from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q

from datetime import datetime, timedelta

from student.models import StudentProfile, StudentFriends
from student.forms import StudentProfileForm, StudentEducationForm
from user.views import check_role_student
from user.models import User
from post.models import Post


@login_required(login_url="loginView")
@user_passes_test(check_role_student)
def StudentRegistrationView(request):
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # return redirect("studentRegistrationView")
            student = form.save(commit=False)
            user = request.user
            student.user = user
            student.save()
            messages.success(request, "You have successful regiater yourself.")
            return redirect("homePage")
    else:
        form = StudentProfileForm()
    context = {
        "form": form,
    }
    return render(request, "student/registration.html", context)


def AddEducation(request):
    if request.method == "POST":
        edu_form = StudentEducationForm(request.POST)
        if edu_form.is_valid():
            pass
    else:
        edu_form = StudentEducationForm()
    context = {
        "edu_form": edu_form,
    }
    return render(request, "", context)


@login_required(login_url="loginView")
@user_passes_test(check_role_student)
def StudentProfileView(request):
    user = request.user
    user_profile = StudentProfile.objects.get(user=user)

    # Retrieve all posts ordered by post_date in descending order
    # Annotate each post with the count of likes it has
    posts = posts = (
        Post.objects.filter(user=user)
        .annotate(like_count=Count("postlike"))
        .order_by("-post_date")
    )

    context = {"user": user, "user_profile": user_profile, "posts": posts}
    return render(request, "student/studentProfile.html", context=context)


def StudentFriendsView(request):
    user = request.user
    user_profile = StudentProfile.objects.get(user=user)

    user_friends = StudentFriends.objects.filter(
        Q(student=user_profile) | Q(friend=user_profile), status=StudentFriends.ACCEPTED
    ).distinct()

    for each in user_friends:
        print(each.friend.full_name(), each.accept_request)

    context = {
        "user": user,
        "user_profile": user_profile,
        "user_friends": user_friends,
    }
    return render(request, "student/studentFriends.html", context=context)


@login_required(login_url="loginView")
@user_passes_test(check_role_student)
def AddFriendsView(request):
    # Get the current user
    user = request.user
    user_profile = StudentProfile.objects.get(user=user)

    # Fetch friend IDs of the current user
    friend_ids = StudentFriends.objects.filter(
        Q(student=user_profile) | Q(friend=user_profile)
    ).values_list("friend__user__id", flat=True)

    # Fetch users who are not friends and exclude the current user and friends
    non_friends_users = (
        User.objects.filter(role=User.STUDENT, studentprofile__isnull=False)
        .exclude(pk=user.pk)
        .exclude(pk__in=friend_ids)
    )

    friend_request = StudentFriends.objects.filter(
        friend=user_profile, status=StudentFriends.PENDING
    )

    for each in friend_request:
        print(each.pk)

    friend_id = StudentFriends.objects.filter(student=user_profile)
    for i in friend_id:
        print(i.friend.user.email)

    context = {
        "user": user,
        "user_profile": user_profile,
        "friends_user": non_friends_users,
        "friend_request": friend_request,
    }
    return render(request, "student/addFriends.html", context=context)


def SendFriendRequestView(request, pk=None):
    if pk is None:
        return redirect("addFriendsView")

    # Get the current user
    current_user = request.user
    # Get the friend profile by primary key
    friend_profile = StudentProfile.objects.get(pk=pk)

    # Check if the friend request already exists or not
    existing_request = StudentFriends.objects.filter(
        student=current_user.studentprofile,
        friend=friend_profile,
    ).exists()

    # If the request doesn't already exist, create a new friend request
    if not existing_request:
        send_friend_request = StudentFriends.objects.create(
            student=current_user.studentprofile,
            friend=friend_profile,
            status=StudentFriends.PENDING,
        )
        messages.success(request, "Friend request send successfully")
        return redirect("addFriendsView")

    messages.success(request, "Friend request already send")
    return redirect("addFriendsView")


def AcceptFriendRequest(request, pk=None):
    print("accept")
    if pk is None:
        return redirect("addFriendsView")

    # Get the current user
    current_user = request.user
    # Get the friend profile by primary key
    friend_profile = StudentProfile.objects.get(pk=pk)

    # Update the friend request status to "Accepted"
    StudentFriends.objects.filter(
        student=friend_profile,
        friend=current_user.studentprofile,
        status=StudentFriends.PENDING,
    ).update(status=StudentFriends.ACCEPTED)

    return redirect("addFriendsView")


def DeclineFriendRequest(request, pk=None):
    if pk is None:
        return redirect("addFriendsView")

    # Get the current user
    current_user = request.user
    # Get the friend profile by primary key
    friend_profile = StudentProfile.objects.get(pk=pk)

    # Update the friend request status to "Accepted"
    StudentFriends.objects.filter(
        student=friend_profile,
        friend=current_user.studentprofile,
        status=StudentFriends.PENDING,
    ).update(status=StudentFriends.DECLINE)

    return redirect("addFriendsView")
