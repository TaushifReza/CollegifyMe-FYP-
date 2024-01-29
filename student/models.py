from django.db import models

from user.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=50)
    cover_image = models.CharField(max_length=50)
    current_address = models.CharField(max_length=250, blank=True, null=True)
    permanent_address = models.CharField(max_length=250, blank=True, null=True)
