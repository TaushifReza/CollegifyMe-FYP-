from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from college.forms import CollegeProfileForm
from user.views import check_role_college


# @login_required(login_url="loginView")
# @user_passes_test(check_role_college)
def CollegeRegistrationView(request):
    if request.method == "POST":
        form = CollegeProfileForm(request.POST, request.FILES)
        if form.is_valid():
            messages.success(request, "Form is valid!!!")
            return redirect("collegeRegistrationView")
    else:
        form = CollegeProfileForm()
    context = {
        "form": form,
    }
    return render(request, "college/collegeRegistration.html", context)
