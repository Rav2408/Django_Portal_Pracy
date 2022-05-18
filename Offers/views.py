import json
import urllib
import urllib.parse
import urllib.request

from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from Django_Portal_Pracy import settings
from .models import Offer
from .forms import CreateUserForm, CreateOfferForm
# from .forms import OfferForm, CreateUserForm, CreateOfferForm
from django.http import HttpResponse
from django.contrib import messages


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'registration/login.html', context)


def logout_view(request):
    logout(request)
    return render(request, "Index/index.html", {})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():

                ''' reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': settings.RECAPTCHA_PRIVATE_KEY,
                    'response': recaptcha_response
                }
                data = urllib.parse.urlencode(values).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())

                if result['success']:
                    form.save()
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password1')
                    messages.success(request, 'Account was created for ' + username)
                    user = authenticate(username=username, password=password)
                    login(request, user)
                else:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')

                return redirect('home')

        else:
            form = CreateUserForm()  # to ta z polem emaila

        form = CreateUserForm()  # to ta z polem emaila
        context = {'form': form}
        return render(request, 'registration/register.html', context)


def home(request):
    return render(request, "Index/index.html", {})


def about(request):
    return render(request, "Index/about.html", {})


def contact(request):
    return render(request, "Index/contact.html", {})


def profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateOfferForm(request.POST)
            if form.is_valid():
                form.save(request)
                return redirect('home')

        else:
            form = CreateOfferForm()

    context = {'form': form}
    return render(request, "Index/profile.html", context)


def jobs(request):
    offersList = Offer.objects.all()
    return render(request, "Offers/jobs.html", {'offers_list': offersList})


def job_details(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'Offers/job-details.html', {'offer': offer})  # 'company': offer.company.email


# /offer_id wyświetla stronę ze szczegółami na temat tej oferty
def detail(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'Offers/detail.html', {'offer': offer})


# tworzysz zmienną przechowującą liste obiektów a następnie
# przekazujesz ją do pliku HTML pod nazwą zadeklarowaną w cudzysłowach (3 parametr render)
def offers_list(request):
    offersList = Offer.objects.all()
    return render(request, 'Offers/offers_list.html', {'offers_list': offersList})
