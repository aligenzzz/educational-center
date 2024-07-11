from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
import uuid
from utilities.validators import phone_validator
    

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(validators=[phone_validator], max_length=13, blank=True, null=True)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ])
    
    def clean(self):
        super().clean()
        if self.role != 'admin' and not self.phone_number:
            raise ValidationError('Phone number is required for non-admin users.')
        
    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-date_joined', )

    def __str__(self):
        return self.username
    
    
class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    photo = models.ImageField(upload_to='teachers/', null=True, blank=True)
    education = models.TextField(max_length=500, null=False, blank=False)
    experience = models.TextField(max_length=1000, null=False, blank=False)
    
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        
    @property
    def full_name(self):
        return f"{self.user.last_name} {self.user.first_name} {self.user.patronymic}"

    def __str__(self):
        return self.full_name
