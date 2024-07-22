from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed


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
