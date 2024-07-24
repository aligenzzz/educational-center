from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import User


class UserModelTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='testpass', role='student')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass'))
        self.assertEqual(user.role, 'student')

    def test_create_admin_user(self):
        admin_user = User.objects.create_user(username='adminuser', password='adminpass', role='admin')
        self.assertTrue(admin_user.is_staff)

    def test_non_admin_user_without_phone(self):
        user = User(username='nouser', role='teacher')
        user.set_password('nopass')
        with self.assertRaises(ValidationError):
            user.clean()
            user.save()

    def test_non_admin_user_with_phone(self):
        try:
            user = User.objects.create_user(username='teacheruser', password='teachpass', role='teacher',
                                            phone_number='+1234567890')
        except ValidationError as e:
            self.fail(f"User creation failed with validation error: {e}")
        self.assertEqual(user.phone_number, '+1234567890')

    def test_admin_user_without_phone(self):
        admin_user = User.objects.create_user(username='adminnop', password='adminpass', role='admin')
        self.assertIsNone(admin_user.phone_number)

    def test_clean_method_validation(self):
        user = User(username='cleanuser', role='student', phone_number=None)
        with self.assertRaises(ValidationError) as cm:
            user.clean()
        self.assertIn('Phone number is required for non-admin users.', str(cm.exception))
