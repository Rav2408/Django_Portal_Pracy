from django.contrib import admin
from django.utils.html import format_html


from .models import Company, Offer, Application
# Register your models here.


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = []


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # fields = ('image_tag',)
    # readonly_fields = ('image_tag',)
    list_display = [ 'company_name', 'logo']


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['company', 'position', 'min_salary', 'max_salary', 'remote', 'location', 'description']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['offer','first_name', 'last_name', 'email', 'cv']
