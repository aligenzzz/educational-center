from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, PasswordChangeSerializer, UserCreateSerializer, UserUpdateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        else:
            return UserSerializer

    @action(detail=True, methods=['POST'], url_path='change-password')
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data.get('password')
        user.set_password(new_password)
        user.save()

        # Возвращаем данные пользователя с паролем
        response_data = {
            'id': str(user.id),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'patronymic': user.patronymic,
            'phone_number': user.phone_number,
            'role': user.role,
            'password': new_password  # Вернуть новый пароль в ответе
        }
        return Response(response_data, status=status.HTTP_200_OK)