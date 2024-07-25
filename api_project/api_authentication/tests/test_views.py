from unittest.mock import patch

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Test',
            last_name='User',
            role='student'
        )
        self.url_list = reverse('users-list')
        self.url_detail = reverse('users-detail', kwargs={'pk': self.user.pk})
        self.client = self.client_class()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_list_users(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['username'], 'testuser')
        self.assertIn('email', response_data[0])
        self.assertEqual(response_data[0]['email'], '')
        self.assertIn('first_name', response_data[0])
        self.assertEqual(response_data[0]['first_name'], 'Test')
        self.assertIn('last_name', response_data[0])
        self.assertEqual(response_data[0]['last_name'], 'User')

    def test_retrieve_user(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['username'], 'testuser')
        self.assertIn('email', response_data)
        self.assertEqual(response_data['email'], '')
        self.assertIn('first_name', response_data)
        self.assertEqual(response_data['first_name'], 'Test')
        self.assertIn('last_name', response_data)
        self.assertEqual(response_data['last_name'], 'User')


class UserProfileViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        self.url = reverse('profile')
        self.client = self.client_class()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('email', response_data)
        self.assertEqual(response_data['email'], '')
        self.assertIn('first_name', response_data)
        self.assertEqual(response_data['first_name'], 'Test')
        self.assertIn('last_name', response_data)
        self.assertEqual(response_data['last_name'], 'User')

    def test_update_profile(self):
        data = {'first_name': 'Updated'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_partial_update_profile(self):
        data = {'first_name': 'Updated'}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')


class ChangePasswordViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='oldpassword'
        )
        self.url = reverse('change-password')
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.client.force_authenticate(user=self.user)

    @patch('api_authentication.views.ChangePasswordSerializer.save', autospec=True)
    @patch('api_authentication.views.JWTSessionAuthentication.authenticate')
    def test_change_password(self, mock_authenticate, mock_save):
        mock_authenticate.return_value = (self.user, None)

        def save_side_effect(serializer, *args, **kwargs):
            user = serializer.context['request'].user
            user.set_password(serializer.validated_data['new_password'])
            user.save()

        mock_save.side_effect = save_side_effect

        data = {
            'old_password': 'oldpassword',
            'new_password': 'newpassword',
            'confirm_new_password': 'newpassword',
            'refresh': self.refresh_token
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))


class LoginViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.url = reverse('token-obtain-pair')  # Обновлено с 'login' на 'token-obtain-pair'

    def test_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())


class LogoutViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.login_url = reverse('token-obtain-pair')
        self.logout_url = reverse('token-blacklist')

        # Получение токенов для пользователя
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_logout(self):
        # Добавление токена в заголовок для аутентификации
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Отправка запроса на логаут
        data = {'refresh': self.refresh_token}
        response = self.client.post(self.logout_url, data, format='json')

        # Проверка, что статус-код ответа соответствует ожиданиям
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TokenViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.url_obtain = reverse('token-obtain-pair')
        self.url_refresh = reverse('token-refresh')
        self.url_verify = reverse('token-verify')
        self.url_blacklist = reverse('token-blacklist')

    def test_obtain_token(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url_obtain, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())
        self.refresh_token = response.json()['refresh']

    def test_refresh_token(self):
        self.test_obtain_token()  # Получаем refresh token для теста
        data = {'refresh': self.refresh_token}
        response = self.client.post(self.url_refresh, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())

    def test_verify_token(self):
        self.test_obtain_token()  # Получаем access token для теста
        access_token = self.client.post(self.url_obtain, {'username': 'testuser', 'password': 'testpassword'}, format='json').json()['access']
        data = {'token': access_token}
        response = self.client.post(self.url_verify, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_blacklist_token(self):
        # Получаем access и refresh токены
        obtain_response = self.client.post(self.url_obtain, {'username': 'testuser', 'password': 'testpassword'},
                                           format='json')
        self.assertEqual(obtain_response.status_code, status.HTTP_200_OK)
        self.refresh_token = obtain_response.json()['refresh']

        # Отправляем запрос на черный список
        data = {'refresh': self.refresh_token}
        response = self.client.post(self.url_blacklist, data,
                                    HTTP_AUTHORIZATION='Bearer ' + obtain_response.json()['access'], format='json')

        # Проверяем статус ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)