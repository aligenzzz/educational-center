from datetime import datetime
from django.utils.timezone import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from api_authentication.models import Teacher, CustomUser
from utilities.validators import phone_validator
import uuid


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='certificates/', null=False, blank=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False, blank=False,
                                related_name='certificates')

    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'

    def __str__(self):
        return f"Certificate ({self.teacher})"


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    creation_date = models.DateField(blank=False, null=False, default=datetime.now)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ('-creation_date', )

    def __str__(self):
        return self.title


class CourseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'CourseCategory'
        verbose_name_plural = 'CourseCategories'
        ordering = ('-name', )

    def __str__(self):
        return self.name
    
    
class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    advantages = models.TextField(blank=True, null=True)
    curriculum = models.TextField(blank=True, null=True)
    study_hours = models.IntegerField(blank=False, null=False, default=0)
    price_for_one = models.PositiveIntegerField(blank=False, null=False)
    price_for_many = models.PositiveIntegerField(blank=False, null=False)
    teachers = models.ManyToManyField(Teacher, blank=True, related_name='courses')
    students = models.ManyToManyField(CustomUser, blank=True, related_name='courses')
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ('-name', )

    def __str__(self):
        return self.name
    
    
class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    percent = models.PositiveIntegerField(blank=False, null=True, default=0, validators=[MaxValueValidator(100)])
    description = models.TextField(max_length=500, blank=False, null=False)

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'
        ordering = ('-percent', )

    def __str__(self):
        return f"{self.percent} %"
   
    
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(max_length=50, blank=False, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=False)
    content = models.TextField(max_length=1000, blank=False, null=False)
    creation_date = models.DateField(blank=False, null=False, default=datetime.now)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ('-creation_date', )

    def __str__(self):
        return f"Review by {self.author} on {self.course_category}"


class FaqCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    class Meta:
        verbose_name = 'FaqCategory'
        verbose_name_plural = 'FaqCategories'
        ordering = ('-name', )

    def __str__(self):
        return self.name


class Faq(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=200, blank=False, null=False)
    answer = models.TextField(max_length=1000, blank=False, null=False)
    faq_category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        verbose_name = 'Faq'
        verbose_name_plural = 'Faq\'s'

    def __str__(self):
        return self.question


class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    surname = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.CharField(validators=[phone_validator], max_length=13, blank=False, null=False)
    email = models.EmailField(blank=True, null=True)
    start_date = models.DateField(blank=False, null=False, default=datetime.now)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ('start_date', )

    def __str__(self):
        return f"{self.name} {self.surname} — {self.course.title}"

    def clean(self):
        super().clean()
        if self.start_date > timezone.now().date():
            raise ValidationError('Start date cannot be in the future.')
        