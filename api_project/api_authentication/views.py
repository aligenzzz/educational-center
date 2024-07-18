from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from .models import User
from .serializers import (
    UserSerializer, PasswordChangeSerializer, UserUpdateSerializer, LoginSerializer
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
    
    
class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(responses={200: UserSerializer()})
    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserUpdateSerializer()}
    )
    def update(self, request, pk=None):
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='post',
        request_body=PasswordChangeSerializer,
        responses={
            200: 'Password changed successfully',
            400: openapi.Response(description='Bad request', examples={
                'application/json': {
                    'error': 'Some error message'
                }
            })
        }
    )
    @action(detail=True, methods=['POST'], url_path='change_password')
    def change_password(self, request, pk=None):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    authentication_classes = [SessionAuthentication]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            }
        ),
        responses={
            200: 'Authentication successful',
            400: openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'errors': {},
                    }
                }
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                'X-CSRFToken',
                openapi.IN_HEADER,
                description='CSRF Token',
                type=openapi.TYPE_STRING
            )
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # authorization inside api
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return Response(status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            204: 'Logout successful',
            400: openapi.Response(
                description='Bad request',
                examples={
                    'application/json': {
                        'error': 'Some error',
                    }
                }
            ),
        },
        manual_parameters=[
            openapi.Parameter(
                'X-CSRFToken',
                openapi.IN_HEADER,
                description='CSRF Token',
                type=openapi.TYPE_STRING
            )
        ]
    )
    def post(self, request):
        try:
            # logout inside api
            logout(request)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class TokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description='Token obtained',
                examples={
                    'application/json': {
                        'access': 'eyJ0eXAiOiJKV1QiLCJh...jzeA',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJh...7Sw',
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description='Token refreshed',
                examples={
                    'application/json': {
                        'access': 'eyJ0eXAiOiJKV1QiLCJh...jzeA',
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            200: 'Token is valid'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        responses={
            200: 'Token blacklisted',
            400: 'Bad request'
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': request.COOKIES['csrftoken']})
