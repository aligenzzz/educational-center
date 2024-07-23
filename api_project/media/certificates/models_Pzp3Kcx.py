from django.db import models


class Client(models.Model):
    nickname = models.CharField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, default=1)
    slug = models.SlugField(max_length=100, unique=True)


class Role(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    slug = models.SlugField(max_length=70, unique=True)
