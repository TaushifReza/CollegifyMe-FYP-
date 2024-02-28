from django.db import models
from django.utils import timezone
from django.template.defaultfilters import timesince

from cloudinary.models import CloudinaryField

from user.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    def time_since_posted(self):
        """
        Returns how long ago the post was posted.
        """
        return timesince(self.post_date, timezone.now())


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    media_file = CloudinaryField("postMedia", blank=True, null=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_date_time = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date_time = models.DateTimeField(auto_now_add=True)
