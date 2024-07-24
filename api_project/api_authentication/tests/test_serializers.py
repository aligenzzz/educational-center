from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.test import APIRequestFactory

from ..serializers import UserSerializer, UserProfileSerializer, ChangePasswordSerializer, LoginSerializer, \
    LogoutSerializer
from ..models import User


class TestUserSerializers(TestCase):

    def setUp(self):
        # self.factory = APIRequestFactory()
        # Create a user for testing purposes
        self.user = User.objects.create_user(username='testuser', password='testpass', role='student')

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['role'], 'student')

    def test_user_profile_serializer_update(self):
        # Create a user to update
        user = User.objects.create_user(
            username='profileuser',
            password='profilepass',
            role='student',
            phone_number='+375765432188'
        )

        data = {
            'username': 'updatedprofileuser',
            'email': 'updated@user.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'patronymic': 'U',
            'phone_number': '+375765432188'
        }

        # Instantiate the serializer with the user instance and update data
        serializer = UserProfileSerializer(user, data=data, partial=True)  # Use partial=True for partial updates

        # Check if the serializer is valid
        if not serializer.is_valid():
            # Print validation errors for debugging
            print("Serializer errors:", serializer.errors)

        self.assertTrue(serializer.is_valid(), "Serializer should be valid")

        # Save the user if the serializer is valid
        updated_user = serializer.save()

        # Verify that the user fields have been updated correctly
        self.assertEqual(updated_user.username, user.username)  # username is not updated
        self.assertEqual(updated_user.email, data['email'])
        self.assertEqual(updated_user.first_name, data['first_name'])
        self.assertEqual(updated_user.last_name, data['last_name'])
        self.assertEqual(updated_user.patronymic, data['patronymic'])
        self.assertEqual(updated_user.phone_number, data['phone_number'])

    def test_change_password_serializer(self):
        User = get_user_model()
        user = User.objects.create_user(username='changepassuser', password='oldpass', role='student')

        data = {
            'old_password': 'oldpass',
            'new_password': 'newpass',
            'confirm_new_password': 'newpass',
            'refresh': 'dummy_refresh_token'
        }

        factory = APIRequestFactory()
        request = factory.post('/change-password/', data=data, format='json')
        request.user = user
        request.META['HTTP_AUTHORIZATION'] = 'Bearer dummy_access_token'

        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = status.HTTP_200_OK
            serializer = ChangePasswordSerializer(data=data, context={'request': request})
            self.assertTrue(serializer.is_valid())
            serializer.save()
            self.assertTrue(user.check_password('newpass'))

    def test_login_serializer(self):
        user = User.objects.create_user(username='loginuser', password='loginpass', role='student')
        data = {
            'username': 'loginuser',
            'password': 'loginpass'
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        authenticated_user = serializer.validated_data
        self.assertEqual(authenticated_user.username, 'loginuser')

    @patch('api_authentication.serializers.requests.post')  # Мокинг requests.post
    @patch('api_authentication.serializers.reverse')  # Мокинг reverse
    def test_logout_serializer(self, mock_reverse, mock_requests_post):
        # Создайте фальшивый объект запроса
        fake_request = MagicMock()
        fake_request.data = {'refresh': 'dummy_refresh_token'}
        fake_request.META = {'HTTP_AUTHORIZATION': 'Bearer dummy_access_token'}

        # Настройте mock для reverse
        mock_reverse.return_value = 'token-blacklist'

        # Настройте mock для build_absolute_uri
        fake_request.build_absolute_uri = MagicMock(return_value='https://example.com/blacklist/')

        # Настройте mock для requests.post
        mock_requests_post.return_value = MagicMock(status_code=status.HTTP_200_OK)  # Успешный ответ

        # Передайте этот фальшивый запрос в контекст
        serializer = LogoutSerializer(data={'refresh': 'dummy_refresh_token'}, context={'request': fake_request})

        # Проверьте, что сериализатор валидный
        self.assertTrue(serializer.is_valid())

        try:
            # Попробуйте сохранить данные
            serializer.save()
        except DRFValidationError:
            self.fail("LogoutSerializer failed with ValidationError")
        except Exception as e:
            self.fail(f"LogoutSerializer raised an unexpected exception: {str(e)}")
