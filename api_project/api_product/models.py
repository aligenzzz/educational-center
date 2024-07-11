import uuid
from django.utils.timezone import timezone

from django.core.exceptions import ValidationError

from api_project.api_authentication.models import Tutor
from django.core.validators import MaxValueValidator
from django.db import models


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(default='no content', blank=False)
    source = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return self.title


class CourseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.title


class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    percent = models.PositiveIntegerField(blank=False, default=0, validators=[MaxValueValidator(100)])
    description = models.TextField(blank=False)

    def __str__(self):
        return self.percent


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(max_length=50, blank=False)
    course_category = models.ForeignKey('CourseCategory', on_delete=models.SET_NULL)
    content = models.TextField(blank=False)

    def __str__(self):
        return f"Review by {self.author} on {self.course_category.title}"


class FAQCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(blank=False)
    description = models.TextField(blank=False)
    faq_category = models.ForeignKey('FAQCategory', on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False)
    surname = models.CharField(max_length=100, blank=False)
    phone_number = models.CharField(max_length=13, blank=False)
    email = models.EmailField(blank=False)
    start_date = models.DateField(blank=False)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} {self.surname} — {self.course.title}"

    def clean(self):
        if self.start_date > timezone.now().date():
            raise ValidationError("Start date cannot be in the future.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure clean() is called before saving
        super(Application, self).save(*args, **kwargs)




class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField()
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    advantages = models.TextField(blank=True)
    curriculum = models.TextField(blank=True)
    study_hours = models.IntegerField(blank=False, default=0)
    price_for_one = models.PositiveIntegerField()
    price_in_group = models.PositiveIntegerField()
    tutors = models.ManyToManyField('Tutor')
    course_category = models.ForeignKey('CourseCategory', on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
