# test_signals.py
from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import User
from ..signals import add_staff_permissions


class UserSignalTest(TestCase):
    def test_add_staff_permissions(self):
        # Убедимся, что изначально у нас есть разрешения
        initial_permission_count = Permission.objects.count()
        self.assertTrue(initial_permission_count > 0, "Expected some permissions to be available")

        # Создаем нового пользователя
        new_staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)

        # Обновляем объект пользователя, чтобы сигнал сработал
        new_staff_user.refresh_from_db()

        # Проверяем, что новому пользователю были назначены все разрешения
        user_permissions = new_staff_user.user_permissions.all()
        self.assertEqual(user_permissions.count(), initial_permission_count,
                         "User should have all permissions assigned")

        # Проверяем конкретные разрешения для убедительности
        for permission in Permission.objects.all():
            self.assertIn(permission, user_permissions, f"Permission {permission} should be assigned to the user")

    def test_no_permissions_for_non_staff(self):
        # Создаем нового обычного пользователя
        new_user = User.objects.create_user(username='regularuser', password='password', is_staff=False)

        # Обновляем объект пользователя, чтобы сигнал сработал
        new_user.refresh_from_db()

        # Проверяем, что новому обычному пользователю не назначены разрешения
        user_permissions = new_user.user_permissions.all()
        self.assertEqual(user_permissions.count(), 0, "Non-staff user should not have any permissions assigned")
