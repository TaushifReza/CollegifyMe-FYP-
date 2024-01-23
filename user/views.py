from django.shortcuts import render


def LoginView(request):
    return render(request, "account/login.html")


def RegisterView(request):
    return render(request, "account/register.html")


def ForgetPassword(request):
    return render(request, "account/forgetPassword.html")
