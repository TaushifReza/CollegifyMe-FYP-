from django.shortcuts import render

# Create your views here.


def StudentRegistrationView(request):
    return render(request, "student/registration.html")
