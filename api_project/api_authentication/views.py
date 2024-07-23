from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from .models import User
from .serializers import (
    UserSerializer, ChangePasswordSerializer, UserProfileSerializer, 
    LoginSerializer, LogoutSerializer
)
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from api_authentication.permissions import JWTSessionAuthentication
    
    
class UserViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    @swagger_auto_schema(
        tags=['Users'],
        responses={
            200: UserSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Users'],
        responses={
            200: UserSerializer,
        },
    )
    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    
class UserProfileView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Profile'],
        responses={
            200: UserProfileSerializer,
            401: 'Unauthorized',
        },
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['Profile'],
        request_body=UserProfileSerializer,
        responses={
            200: openapi.Response(
                description='Profile was updated',
                schema=UserProfileSerializer,
            ),
            400: 'Bad request',
            401: 'Unauthorized',
        },
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Profile'],
        request_body=UserProfileSerializer,
        responses={
            200: openapi.Response(
                description='Profile was updated',
                schema=UserProfileSerializer,
            ),
            400: 'Bad request',
            401: 'Unauthorized',
        },
    )
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ChangePasswordView(views.APIView):
    authentication_classes = [JWTSessionAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Profile'],
        request_body=ChangePasswordSerializer,
        responses={
            204: 'Password changed successfully',
            400: 'Bad request',
            401: 'Unauthorized',
        },
        manual_parameters=[
            openapi.Parameter(
                'X-CSRFToken',
                openapi.IN_HEADER,
                description='CSRF Token',
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        tags=['Auth'],
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description='Authentication successful',
                examples={
                    'application/json': {
                        'access': 'eyJ0eXAiOiJKV1QiLCJh...jzeA',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJh...7Sw',
                    }
                }
            ),
            400: 'Bad request',
        },
        manual_parameters=[
            openapi.Parameter(
                'X-CSRFToken',
                openapi.IN_HEADER,
                description='CSRF Token',
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                tokens = serializer.save()
                return Response(tokens, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    authentication_classes = [JWTSessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=['Auth'],
        request_body=LogoutSerializer,
        responses={
            204: 'Logout successful',
            400: 'Bad request',
            401: 'Unauthorized',
        },
        manual_parameters=[
            openapi.Parameter(
                'X-CSRFToken',
                openapi.IN_HEADER,
                description='CSRF Token',
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TokenObtainPairView(TokenObtainPairView): 
    authentication_classes=[]
    permission_classes = [AllowAny]
      
    @swagger_auto_schema(
        tags=['Auth'],
        responses={
            200: openapi.Response(
                description='Token obtained',
                examples={
                    'application/json': {
                        'access': 'eyJ0eXAiOiJKV1QiLCJh...jzeA',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJh...7Sw',
                    }
                }
            ),
            401: 'Unauthorized',
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(TokenRefreshView):
    authentication_classes=[]
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        tags=['Auth'],
        responses={
            200: openapi.Response(
                description='Token refreshed',
                examples={
                    'application/json': {
                        'access': 'eyJ0eXAiOiJKV1QiLCJh...jzeA',
                    }
                }
            ),
            401: 'Unauthorized',
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyView(TokenVerifyView):
    authentication_classes=[]
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        tags=['Auth'],
        responses={
            200: 'Token is valid',
            401: 'Unauthorized',
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenBlacklistView(TokenBlacklistView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=['Auth'],
        responses={
            200: 'Token blacklisted',
            401: 'Unauthorized',
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': request.COOKIES['csrftoken']})
