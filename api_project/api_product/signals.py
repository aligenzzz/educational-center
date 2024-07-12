from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from api_product.models import Course
from api_authentication.models import User
from django.core.exceptions import ValidationError


@receiver(m2m_changed, sender=Course.students.through)
def validate_students(sender, instance, action, **kwargs):
    if action == 'pre_add':
        for student_id in kwargs['pk_set']:
            student = User.objects.get(pk=student_id)
            if student.role != 'student':
                raise ValidationError(f"User {student.username} does not have the 'student' role")
            