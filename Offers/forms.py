from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Offer, Company

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


# class OfferForm(ModelForm):
#    class Meta:
#        model = Offer
#        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        feedback = forms.CharField(widget=forms.Textarea)
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class CreateOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'company',
            'position',
            'min_salary',
            'max_salary',
            'remote',
            'location',
            'description'
        ]

    def save(self, request):
        self.instance.author = request.user
        saved_data = super().save()
        request.session['new_offer_id'] = self.instance.id
        return saved_data

class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'company_name',
            'city',
            'street',
            'street_number',
            'postcode',
            'suite_number',
            'email',
            'social_links',
            'logo',
            'phone'
        ]

    def save(self, request):
        self.instance.author = request.user
        saved_data = super().save()
        request.session['new_company_id'] = self.instance.id
        return saved_data
