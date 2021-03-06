from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension, file_size
from django.db.models import DO_NOTHING



class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    company_name = models.CharField('company_name', max_length=30, blank=False)
    city = models.CharField('city', max_length=20, blank=False)
    street = models.CharField('street', max_length=20, blank=False)
    street_number = models.IntegerField(blank=False)
    postcode = models.CharField('postcode', max_length=6, blank=False)
    suite_number = models.IntegerField(blank=True, null=True)
    email = models.EmailField('email', blank=False)
    social_links = models.URLField(null=True)
    logo = models.ImageField(upload_to="logo/", validators=[file_size], null=True, blank=True, default=None)
    phone = models.CharField('phone', max_length=20, blank=False, default=None)

    def __str__(self):
        return self.company_name

    def company_id(self):
        return self.id

    def delete(self, *args, **kwargs):
        self.logo.delete()
        super().delete(*args, **kwargs)



        # def image_tag(self):  # new
        #     return mark_safe('<img src="/../../static/logo/%s" width="150" height="150" />' % (self.logo))

    # def save(self, *args, **kwargs):
    #     super().save()
    #
    #     img = Image.open(self.logo.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size) # resizes image (thumbnails are reduced-size versions of pictures)
    #         img.save(self.logo.path)


class Offer(models.Model):
    company = models.ForeignKey(Company, on_delete=DO_NOTHING)
    position = models.CharField('position', max_length=50, blank=False)
    min_salary = models.IntegerField(blank=True)
    max_salary = models.IntegerField(blank=True)
    remote = models.BooleanField(default=False)
    location = models.CharField('location', max_length=50, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)

    def offer_id(self):
        return self.id


class Application(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    first_name = models.CharField(('first name'), max_length=30, blank=False, default=None)
    last_name = models.CharField(('last name'), max_length=30, blank=False, default=None)
    email = models.EmailField('email', blank=True, default=None)
    cv = models.FileField(upload_to='uploads/', validators=[validate_file_extension, file_size], default=None)
    reason = models.TextField('reason', max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.offer

    def offer_id(self):
        return self.id

    def delete(self, *args, **kwargs):
        self.cv.delete()
        super().delete(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     super().save()
    #     img = Image.open(self.logo.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size) # resizes image (thumbnails are reduced-size versions of pictures)
    #         img.save(self.logo.path)


#
# class Tag(models.Model):
#     name = models.CharField(max_length = 50)
#
#     def __str__(self):
#         return self.name