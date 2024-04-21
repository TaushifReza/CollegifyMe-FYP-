from django.test import TestCase
from django.contrib.auth import get_user_model

from college.models import CollegeProfile

User = get_user_model()


class CollegeProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="password"
        )
        self.college_profile = CollegeProfile.objects.create(
            user=self.user,
            college_name="Test College",
            college_slug="test-college",
            college_logo="path/to/logo.png",
            cover_image="path/to/cover_image.png",
            website_url="http://www.testcollege.com",
            address="Test Address",
            phone_number="1234567890",
        )

    def test_college_profile_creation(self):
        self.assertIsNotNone(self.college_profile)
        self.assertEqual(self.college_profile.college_name, "Test College")
        self.assertEqual(self.college_profile.college_slug, "test-college")
        self.assertEqual(self.college_profile.college_logo, "path/to/logo.png")
        self.assertEqual(self.college_profile.cover_image, "path/to/cover_image.png")
        self.assertEqual(self.college_profile.website_url, "http://www.testcollege.com")
        self.assertEqual(self.college_profile.address, "Test Address")
        self.assertEqual(self.college_profile.phone_number, "1234567890")
