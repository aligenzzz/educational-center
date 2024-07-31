from django.test import TestCase
from ..forms import UserCreationForm, UserChangeForm
from ..models import User


class UserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'patronymic': 'Middle',
            'email': 'newuser@example.com',
            'phone_number': '+375456789022',
            'role': 'student',
            'password1': 'complexpassword',
            'password2': 'complexpassword'
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email',
            'phone_number': 'not-a-number',
            'role': '',
            'password1': 'complexpassword',
            'password2': 'differentpassword'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserChangeFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            patronymic='Middle',
            email='testuser@example.com',
            phone_number='+375338787877',
            role='student',
            password='complexpassword'
        )

    def test_valid_form(self):
        form_data = {
            'username': 'changeduser',
            'first_name': 'Changed',
            'last_name': 'User',
            'patronymic': 'Middle',
            'email': 'changeduser@example.com',
            'phone_number': '+375338787876',
            'role': 'teacher'
        }
        form = UserChangeForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email',
            'phone_number': 'not-a-number',
            'role': ''
        }
        form = UserChangeForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
