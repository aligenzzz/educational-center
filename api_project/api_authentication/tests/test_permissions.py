from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from ..models import User
from api_product.models import Certificate, TeacherInfo
from ..permissions import JWTSessionAuthentication, IsAdminOrOwnerTeacher


class TestPermissions(TestCase):

    def setUp(self):
        # Создание пользователей и данных
        self.student = User.objects.create_user(username='student', password='password', role='student')
        self.admin = User.objects.create_user(username='admin', password='password', role='admin', is_staff=True)
        self.teacher_user = User.objects.create_user(username='teacher', password='password', role='teacher')

        self.teacher_info = TeacherInfo.objects.create(
            user=self.teacher_user,
            education="Some education details",
            experience="Some experience details"
        )

        self.certificate = Certificate.objects.create(
            teacher=self.teacher_info,
            file='path/to/file.pdf'
        )

        self.jwt_authenticator = JWTSessionAuthentication()
        self.factory = RequestFactory()

        self.refresh = RefreshToken.for_user(self.student)
        self.access_token = str(self.refresh.access_token)

    @patch('api_authentication.permissions.JWTAuthentication')
    @patch('api_authentication.permissions.SessionAuthentication')
    def test_jwt_authentication(self, MockSessionAuth, MockJWTAuth):
        # Настройка моков
        mock_jwt_auth = MockJWTAuth.return_value
        mock_jwt_auth.authenticate.return_value = (self.student, None)

        mock_session_auth = MockSessionAuth.return_value
        mock_session_auth.authenticate.return_value = (self.student, None)

        request = MagicMock()
        request.META = {'HTTP_AUTHORIZATION': 'Bearer valid_token'}

        # Проверка аутентификации
        user_auth_tuple = self.jwt_authenticator.authenticate(request)
        self.assertEqual(user_auth_tuple[0], self.student)

        # Изменение поведения мока для проверки неудачной аутентификации
        mock_jwt_auth.authenticate.return_value = None
        with self.assertRaises(AuthenticationFailed):
            self.jwt_authenticator.authenticate(request)

    def authenticate_with_session(self, user):
        factory = RequestFactory()
        request = factory.get('/')
        request.user = user
        request.session = MagicMock()  # Мокируем сессию
        return request

    @patch('api_authentication.permissions.JWTAuthentication')
    @patch('api_authentication.permissions.SessionAuthentication')
    def test_session_authentication(self, MockSessionAuth, MockJWTAuth):
        # Настройка моков
        mock_jwt_auth = MockJWTAuth.return_value
        mock_jwt_auth.authenticate.return_value = (self.student, None)

        mock_session_auth = MockSessionAuth.return_value
        mock_session_auth.authenticate.return_value = (self.student, None)

        # Создаем запрос с сессией
        request = MagicMock()
        request.session = MagicMock()  # Мокируем сессию
        request.user = self.student

        # Проверка аутентификации сессии
        user_auth_tuple = JWTSessionAuthentication().authenticate(request)
        self.assertEqual(user_auth_tuple[0], self.student)

        # Изменение поведения мока для проверки неудачной аутентификации
        mock_session_auth.authenticate.return_value = None
        with self.assertRaises(AuthenticationFailed):
            JWTSessionAuthentication().authenticate(request)

    def test_is_admin_or_owner_teacher_permission(self):
        permission = IsAdminOrOwnerTeacher()

        # As admin
        request = self.factory.get('/')
        request.user = self.admin
        self.assertTrue(permission.has_permission(request, None))
        self.assertTrue(permission.has_object_permission(request, None, self.certificate))

        # As teacher (owner)
        request.user = self.teacher_user
        self.assertTrue(permission.has_permission(request, None))
        self.assertTrue(permission.has_object_permission(request, None, self.certificate))

        # As student (not owner)
        request.user = self.student
        self.assertTrue(permission.has_permission(request, None))
        self.assertFalse(permission.has_object_permission(request, None, self.certificate))



