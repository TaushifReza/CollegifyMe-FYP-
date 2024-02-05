from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify

from college.forms import CollegeProfileForm
from user.views import check_role_college


@login_required(login_url="loginView")
@user_passes_test(check_role_college)
def CollegeRegistrationView(request):
    if request.method == "POST":
        form = CollegeProfileForm(request.POST, request.FILES)
        if form.is_valid():
            college = form.save(commit=False)
            user = request.user
            college.user = user
            college_name = form.cleaned_data["college_name"]
            college.college_slug = slugify(college_name) + "-" + str(user.id)
            college.save()
            messages.success(request, "You have successful regiater!!!")
            return redirect("collegeRegistrationView")
    else:
        form = CollegeProfileForm()
    context = {
        "form": form,
    }
    return render(request, "college/collegeRegistration.html", context)
