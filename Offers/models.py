from django.db import models

# ctrl + alt + shift + l
# Create your models here.
from django.db.models import DO_NOTHING


class User(models.Model):
    username = models.CharField(('username'), max_length=20, blank=False)
    password = models.CharField(('password'), max_length=30, blank=False)
    first_name = models.CharField(('first name'), max_length=30, blank=False)
    last_name = models.CharField(('last name'), max_length=30, blank=False)
    email = models.EmailField(('email address'), blank=True)
    cv = models.FileField(upload_to='uploads/')
    social_links = models.URLField(null=True)

class Company(models.Model):
    username = models.CharField(('username'), max_length=20, blank=False)
    password = models.CharField(('password'), max_length=30, blank=False)
    company_name = models.CharField(('password'), max_length=30, blank=False)
    city = models.CharField(('city'), max_length=20, blank=False)
    street = models.CharField(('street'), max_length=20, blank=False)
    street_number = models.IntegerField(blank=False)
    postcode = models.CharField(('postcode'), max_length=6, blank=False)
    suite_number = models.IntegerField(blank=True)
    email = models.EmailField(('email address'), blank=False)
    social_links = models.URLField(null=True)
    logo = models.ImageField(upload_to = "logo/", null=True, default=None)

class Offer(models.Model):
    company = models.CharField(('username'), max_length=25, blank=False)
    position = models.CharField(('username'), max_length=20, blank=False)
    min_salary = models.IntegerField(blank=True)
    max_salary = models.IntegerField(blank=True)
    remote = models.BooleanField()
    location = models.CharField(('location'), max_length=50, blank=False)
    description = models.TextField(blank=True)

class Application(models.Model):
    offer = models.OneToOneField(Offer, on_delete=DO_NOTHING) #on_delete
    user = models.OneToOneField(User, on_delete=DO_NOTHING)
    response = models.CharField(('response'), max_length=50, blank=True)
