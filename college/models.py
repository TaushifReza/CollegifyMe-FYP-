from django.db import models

from cloudinary.models import CloudinaryField

from user.models import User


class CollegeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=50)
    college_slug = models.SlugField(max_length=100, unique=True)
    college_logo = CloudinaryField("profileImage")
    cover_image = CloudinaryField("coverImage")
    website_url = models.URLField()
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
