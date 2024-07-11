from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
import uuid
    

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(validators=[
        RegexValidator(
            regex=r'^\+375\d{9}$',
            message='Phone number must be entered in the format: +375XXXXXXXXX.',
        )
    ], max_length=13, blank=True, null=True)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('client', 'Client'),
    ])
    
    def clean(self):
        super().clean()
        if self.role != 'admin' and not self.phone_number:
            raise ValidationError('Phone number is required for non-admin users.')
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username
    
    
class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=False, null=False)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to=f'teachers/', null=True, blank=True)
    education = models.TextField(max_length=500, null=False, blank=False)
    experience = models.TextField(max_length=1000, null=False, blank=False)
    
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f'{self.surname} {self.name}'
    
    
class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='certificates/', null=False, blank=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False, blank=False)
    
    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'

    def __str__(self):
        return f'Certificate ({self.teacher})'
