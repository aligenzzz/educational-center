from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from api_product.models import Certificate


class JWTSessionAuthentication:
    def authenticate(self, request):
        jwt_authenticator = JWTAuthentication()
        session_authenticator = SessionAuthentication()
        
        # trying jwt authentication
        user_auth_tuple = jwt_authenticator.authenticate(request)
        if user_auth_tuple is None:
            raise AuthenticationFailed('Invalid or missing JWT token.')

        # trying session (csrf) authentication
        user_auth_tuple = session_authenticator.authenticate(request)
        if user_auth_tuple is None:
            raise AuthenticationFailed('Invalid or missing session authentication.')
            
        return user_auth_tuple

    def authenticate_header(self, request):
        jwt_authenticator = JWTAuthentication()
        return jwt_authenticator.authenticate_header(request)


class IsAdminOrOwnerTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Certificate):
            return request.user.is_staff or obj.teacher.user == request.user
        else:
            return request.user.is_staff or obj.user == request.user
    