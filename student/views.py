from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from student.models import StudentProfile
from student.forms import StudentProfileForm


@login_required(login_url="loginView")
def StudentRegistrationView(request):
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect("studentRegistrationView")
    else:
        form = StudentProfileForm()
    context = {
        "form": form,
    }
    return render(request, "student/registration.html", context)
