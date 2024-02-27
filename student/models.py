from django.db import models

from cloudinary.models import CloudinaryField

from user.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_image = CloudinaryField("profileImage", blank=True, null=True)
    cover_image = CloudinaryField("coverImage", blank=True, null=True)
    current_address = models.CharField(max_length=250, blank=True, null=True)
    permanent_address = models.CharField(max_length=250, blank=True, null=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class StudentEducation(models.Model):
    user = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    level_of_education = models.CharField(max_length=50)
    degree_name = models.CharField(max_length=50)
    college_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()


class StudentFriends(models.Model):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    DECLINE = "Decline"

    FRIEND_REQUEST_CHOICES = (
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (DECLINE, "Decline"),
    )

    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="student"
    )
    friend = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="friend"
    )
    status = models.CharField(max_length=10, choices=FRIEND_REQUEST_CHOICES)

    request_send = models.DateTimeField(auto_now_add=True)
    accept_request = models.DateTimeField(null=True, blank=True)
