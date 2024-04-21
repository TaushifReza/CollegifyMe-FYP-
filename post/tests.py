from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Post


class PostModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(email="test@gmail", password="password123")

    def setUp(self):
        self.post = Post.objects.create(
            user=self.user, post_content="Test post content"
        )

    def test_post_time_since_posted(self):
        self.assertIsInstance(self.post.time_since_posted(), str)

    def test_post_time_since_posted_with_future_date(self):
        future_date = timezone.now() + timezone.timedelta(days=1)
        self.post.post_date = future_date
        self.post.save()

        self.assertEqual(
            self.post.time_since_posted().replace("\xa0", " "), "0 minutes"
        )
