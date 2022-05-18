from django.db import models
from django.contrib.auth.models import User

# ctrl + alt + shift + l
# Create your models here.
from django.db.models import DO_NOTHING


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField('company_name', max_length=30, blank=False)
    city = models.CharField('city', max_length=20, blank=False)
    street = models.CharField('street', max_length=20, blank=False)
    street_number = models.IntegerField(blank=False)
    postcode = models.CharField('postcode', max_length=6, blank=False)
    suite_number = models.IntegerField(blank=True)
    email = models.EmailField('email', blank=False)
    social_links = models.URLField(null=True)
    logo = models.ImageField(upload_to="logo/", null=True, blank=True, default=None)


class Offer(models.Model):
    company = models.CharField('username', max_length=25, blank=False)
    position = models.CharField('position', max_length=20, blank=False)
    min_salary = models.IntegerField(blank=True)
    max_salary = models.IntegerField(blank=True)
    remote = models.BooleanField()
    location = models.CharField('location', max_length=50, blank=False)
    description = models.TextField(blank=True)


class Application(models.Model):
    offer = models.OneToOneField(Offer, on_delete=DO_NOTHING)  # on_delete
    user = models.OneToOneField(Company, on_delete=DO_NOTHING)
    response = models.CharField('response', max_length=50, blank=True)
