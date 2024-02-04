from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from student.models import StudentProfile
from student.forms import StudentProfileForm


@login_required(login_url="loginView")
def StudentRegistrationView(request):
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data["profile_image"])
            # print(form.cleaned_data["cover_image"])
            # print(form.cleaned_data["first_name"])
            # print(form.cleaned_data["last_name"])
            # print(form.cleaned_data["current_address"])
            # print(form.cleaned_data["permanent_address"])
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
