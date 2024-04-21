from django.test import TestCase
from user.models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        self.student_user = User.objects.create(
            email="student@example.com", role=User.STUDENT, is_active=True
        )
        self.college_user = User.objects.create(
            email="college@example.com", role=User.COLLEGE, is_active=True
        )

    def test_email_field(self):
        self.assertEqual(self.student_user.email, "student@example.com")
        self.assertEqual(self.college_user.email, "college@example.com")

    def test_role_field(self):
        self.assertEqual(self.student_user.role, User.STUDENT)
        self.assertEqual(self.college_user.role, User.COLLEGE)
        self.assertEqual(self.student_user.get_role(), "Student")
        self.assertEqual(self.college_user.get_role(), "College")

    def test_date_fields(self):
        self.assertIsNotNone(self.student_user.date_joined)
        self.assertIsNotNone(self.student_user.last_login)
        self.assertIsNotNone(self.student_user.created_date)
        self.assertIsNotNone(self.student_user.modified_date)

    def test_permissions(self):
        self.assertFalse(self.student_user.is_admin)
        self.assertFalse(self.student_user.is_staff)
        self.assertFalse(self.student_user.is_superadmin)
        self.assertFalse(self.student_user.has_perm("test_perm"))
        self.assertTrue(self.student_user.has_module_perms("test_app"))

    def test_str_method(self):
        self.assertEqual(str(self.student_user), "student@example.com")
        self.assertEqual(str(self.college_user), "college@example.com")
