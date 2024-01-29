from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages, auth

from .form import UserForm
from .models import User
from .utils import send_verification_email


def RegisterView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(email=email, password=password)
            user.role = User.STUDENT
            user.save()
            print(email, password)
            # Send Verification email
            mail_subject = "Please activate your account"
            email_template = "account/email/accountVerification.html"
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Please check your mail for verification")
            return redirect("registerView")
    else:
        form = UserForm()
    context = {
        "form": form,
    }
    return render(request, "account/register.html", context)


def activate(request, uidb64, token):
    # Activate the user by setting is_active true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated")
        print("Your account has been activated")
        return redirect("loginView")
    else:
        messages.error(request, "Invalid activation link")
        print("Invalid activation link")
        return redirect("account/register.html")


def LoginView(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            # auth.login(request, user)
            print("Valid Credential")
            return redirect("loginView")
        else:
            messages.error(request, "Invalid Credential")
            return redirect("loginView")
    return render(request, "account/login.html")


def ForgetPassword(request):
    return render(request, "account/forgetPassword.html")
