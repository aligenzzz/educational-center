from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users_api')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', views.TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', views.TokenBlacklistView.as_view(), name='token_blacklist'),
    
    # for login + logout inside api
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
]
