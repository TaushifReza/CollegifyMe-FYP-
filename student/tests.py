from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import StudentProfile, StudentFriends
from django.utils import timezone

User = get_user_model()


class StudentProfileModelTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(
            email="student@example.com", role=User.STUDENT, is_active=True
        )
        # Create a student profile associated with the user
        self.student_profile = StudentProfile.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            current_address="Current Address",
            permanent_address="Permanent Address",
        )

    def test_student_profile_creation(self):
        # Check if the student profile instance is created
        self.assertIsNotNone(self.student_profile)
        # Check if the user is associated with the student profile
        self.assertEqual(self.student_profile.user, self.user)

    def test_student_profile_fields(self):
        # Check the values of various fields
        self.assertEqual(self.student_profile.first_name, "John")
        self.assertEqual(self.student_profile.last_name, "Doe")
        self.assertEqual(self.student_profile.current_address, "Current Address")
        self.assertEqual(self.student_profile.permanent_address, "Permanent Address")

    def test_full_name_method(self):
        # Check the full_name method
        expected_full_name = "John Doe"
        self.assertEqual(self.student_profile.full_name(), expected_full_name)


class StudentFriendsModelTestCase(TestCase):
    def setUp(self):
        self.student1_user = User.objects.create(
            email="john@example.com", password="password"
        )
        self.student2_user = User.objects.create(
            email="jane@example.com", password="password"
        )

        self.student1 = StudentProfile.objects.create(
            user=self.student1_user, first_name="Bicky", last_name="Yadav"
        )
        self.student2 = StudentProfile.objects.create(
            user=self.student2_user, first_name="Hrishik", last_name="Sangrula"
        )
        self.friend_request = StudentFriends.objects.create(
            student=self.student1,
            friend=self.student2,
            status=StudentFriends.PENDING,
        )

    def test_student_friends_creation(self):
        self.assertIsNotNone(self.friend_request)
        self.assertEqual(self.friend_request.student, self.student1)
        self.assertEqual(self.friend_request.friend, self.student2)

    def test_student_friends_fields(self):
        self.assertEqual(self.friend_request.status, StudentFriends.PENDING)

    def test_is_recent_request_property(self):
        self.assertFalse(self.friend_request.is_recent_request)

        self.friend_request.accept_request = timezone.now() - timezone.timedelta(
            days=10
        )
        self.friend_request.save()
        self.assertTrue(self.friend_request.is_recent_request)
