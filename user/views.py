from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages, auth
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password

from .form import UserForm
from .models import User
from .utils import send_verification_email, send_otp_email
from student.models import StudentProfile
from college.models import CollegeProfile


# Restrict student from accessing college page
def check_role_student(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict college from accessing student page
def check_role_college(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def RegisterView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(email=email, password=password)
            user.role = User.STUDENT
            user.save()
            # Send Verification email
            mail_subject = "Please activate your account"
            email_template = "account/email/accountVerification.html"
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Please check your mail for verification")
    else:
        form = UserForm()
    context = {
        "form": form,
    }
    return render(request, "account/register.html", context)


def RegisterCollegeView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(email=email, password=password)
            user.role = User.COLLEGE
            user.save()
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
    return render(request, "account/registerCollege.html", context)


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
            # email and Password is valid
            auth.login(request, user)
            student_profile = StudentProfile.objects.filter(user=user)
            college_profile = CollegeProfile.objects.filter(user=user)
            if student_profile.exists():
                # student have created his profile
                print("Record Found")
                print("User is a Student")
                context = {"user": user, "user_profile": student_profile}
                return redirect("homePage")
            elif college_profile.exists():
                # College have created his profile
                print("Record Found")
                print("User is a College")
                return redirect("homePage")
            else:
                # when both have not created his profile then redirect to respective profile registeration
                if user.role == 1:
                    # user is Student
                    print("User is a Student")
                    return redirect("studentRegistrationView")
                elif user.role == 2:
                    # User is College
                    print("User is a College")
                    return redirect("collegeRegistrationView")
        else:
            # email and password is invalid
            messages.error(request, "Invalid Credential")
            return redirect("loginView")
    return render(request, "account/login.html")


def LogoutView(request):
    auth.logout(request)
    messages.info(request, "You have logout!!!")
    return redirect("loginView")


def ForgetPassword(request):
    return render(request, "account/forgetPassword.html")


def SendOTP(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Corrected line
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email doesn't exist.")
            return render(request, "account/forgetPassword.html")
        mail_subject = "Forgot Password OTP"
        email_template = "account/email/sendOTP.html"
        send_otp_email(request, email, mail_subject, email_template)  # Corrected line
        messages.success(request, "Please check your mail for verification")
        return redirect("verifyOtp")
    return render(request, "account/forgetPassword.html")


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        new_password = request.POST.get("newPassword")
        stored_otp = request.session.get("otp")
        stored_email = request.session.get("email")
        if entered_otp == stored_otp:
            # OTP matched, do something here
            user = User.objects.get(email=stored_email)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password reset successfully!")
            return redirect("loginView")
        else:
            messages.error(request, "Invalid OTP, please try again.")
            return redirect("verifyOtp")
    return render(request, "account/passwordReset.html")
