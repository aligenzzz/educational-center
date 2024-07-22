from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/', views.TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', views.TokenVerifyView.as_view(), name='token-verify'),
    path('token/blacklist/', views.TokenBlacklistView.as_view(), name='token-blacklist'),   
    path('csrf-token/', views.get_csrf_token, name='csrf-token'),
]
