from django.db import models
from api_authentication.models import Teacher
import uuid

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='certificates/', null=False, blank=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False, blank=False)
    
    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'

    def __str__(self):
        return f"Certificate ({self.teacher})"
