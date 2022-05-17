from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Offer
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    feedback = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user
