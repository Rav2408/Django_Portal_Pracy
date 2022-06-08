from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Offer, Company, Application

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
        feedback = forms.CharField(widget=forms.Textarea, required=True)
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, required=True)

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat password'


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['value'] = kwargs['instance'].username
        self.fields['email'].widget.attrs['value'] = kwargs['instance'].email
        self.fields['password'].widget.attrs['value'] = ''
        self.fields['password'].widget.attrs['placeholder'] = 'Password'


class CreateOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'position',
            'min_salary',
            'max_salary',
            'remote',
            'location',
            'description'
        ]


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
    def __init__(self, *args, **kwargs):
        super(CreateCompanyForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs['placeholder'] = 'Company name'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['street'].widget.attrs['placeholder'] = 'Street'
        self.fields['street_number'].widget.attrs['placeholder'] = 'Street number'
        self.fields['postcode'].widget.attrs['placeholder'] = 'Postcode'
        self.fields['suite_number'].widget.attrs['placeholder'] = 'Apartment number'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['social_links'].widget.attrs['placeholder'] = 'Website address'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone number'



class CreateApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['offer']
        feedback = forms.CharField(widget=forms.Textarea, required=True)
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, required=True)
    def __init__(self, *args, **kwargs):
        super(CreateApplicationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['email'].widget.attrs['placeholder'] = 'E-Mail'
        self.fields['reason'].widget.attrs['placeholder'] = 'Additional information'
