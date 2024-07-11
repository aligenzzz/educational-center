from datetime import datetime

from django.utils.timezone import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from api_project.api_authentication.models import Teacher
from api_project.utilities.validators import phone_validator
import uuid


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(default='no content', null=False, blank=False)
    source = models.CharField(max_length=200, default='', null=True, blank=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title


class CourseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    percent = models.PositiveIntegerField(blank=False, null=True, default=0, validators=[MaxValueValidator(100)])
    description = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return f"{self.percent} %"


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(max_length=50, blank=False, null=False)
    course_category = models.ForeignKey('CourseCategory', on_delete=models.SET_NULL, blank=False, null=False)
    content = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"Review by {self.author} on {self.course_category.title}"


class FAQCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class FAQ(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    faq_category = models.ForeignKey('FAQCategory', on_delete=models.SET_NULL, blank=False, null=False)

    class Meta:
        verbose_name = 'FaQ'
        verbose_name_plural = 'FaQs'

    def __str__(self):
        return self.title


class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    surname = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.CharField(validators=[phone_validator], max_length=13, blank=False, null=False)
    email = models.EmailField(blank=False, null=True)
    start_date = models.DateField(blank=False, null=False, auto_now_add=True, default=datetime.now())
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, blank=False, null=False)

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return f"{self.name} {self.surname} — {self.course.title}"

    def clean(self):
        super().clean()
        if self.start_date > timezone.now().date():
            raise ValidationError("Start date cannot be in the future.")


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField()
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    advantages = models.TextField(blank=True, null=True)
    curriculum = models.TextField(blank=True, null=True)
    study_hours = models.IntegerField(blank=False, null=False, default=0)
    price_for_one = models.PositiveIntegerField(blank=False, null=False)
    price_in_group = models.PositiveIntegerField(blank=False, null=False)
    tutors = models.ManyToManyField('Teacher', blank=False, null=False)
    course_category = models.ForeignKey('CourseCategory', on_delete=models.SET_NULL, blank=False, null=False)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.title


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='certificates/', null=False, blank=False)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'

    def __str__(self):
        return f"Certificate ({self.teacher})"
