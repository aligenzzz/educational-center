from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from .models import Course, Certificate
from api_authentication.models import User
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage


@receiver(m2m_changed, sender=Course.students.through)
def validate_students(sender, instance, action, **kwargs):
    if action == 'pre_add':
        for student_id in kwargs['pk_set']:
            student = User.objects.get(pk=student_id)
            if student.role != 'student':
                raise ValidationError(f'User {student.username} does not have the \'student\' role')


@receiver(post_delete, sender=Certificate)
def delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if default_storage.exists(instance.file.name):
            default_storage.delete(instance.file.name)   
                  