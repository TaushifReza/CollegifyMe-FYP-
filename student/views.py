from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from student.models import StudentProfile
from student.forms import StudentProfileForm, StudentEducationForm
from user.views import check_role_student


@login_required(login_url="loginView")
@user_passes_test(check_role_student)
def StudentRegistrationView(request):
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            user = request.user
            student.user = user
            student.save()
            messages.success(request, "You have successful regiater yourself.")
            return redirect("studentRegistrationView")
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

    context = {"user": user, "user_profile": user_profile}
    return render(request, "student/studentProfile.html", context=context)
