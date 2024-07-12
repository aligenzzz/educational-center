from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from utilities.validators import phone_validator
from django.db import models
import uuid
    

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(validators=[phone_validator], max_length=13, blank=True, null=True, unique=True)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ])
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-date_joined',)

    def __str__(self):
        return self.username
    
    def clean(self):
        super().clean()
        if self.role != 'admin' and not self.phone_number:
            raise ValidationError('Phone number is required for non-admin users.')
        
    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
        super().save(*args, **kwargs)
    