import json
import urllib
import urllib.parse
import urllib.request

from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

from Django_Portal_Pracy import settings
from .models import Offer, Company, Application
from .forms import CreateUserForm, CreateOfferForm, CreateCompanyForm, CreateApplicationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView


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
        return redirect('register_company')
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

                return redirect('register_company')

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
                remote = True
                if request.POST.get('remote') is None:
                    remote = False
                offer = Offer(company=get_object_or_404(Company, user=request.user.pk),
                              position=request.POST.get('position'),
                              min_salary=request.POST.get('min_salary'),
                              max_salary=request.POST.get('max_salary'),
                              remote=remote,
                              location=request.POST.get('location'),
                              description=request.POST.get('description')
                              )

                offer.save()
                return redirect('home')

        else:
            form = CreateOfferForm()

    context = {'form': form}
    return render(request, "Index/profile.html", context)


def registerCompany(request, *args, **kwargs):
    if request.method == "POST":
        form = CreateCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = Company(company_name=request.POST.get('company_name'),
                              city=request.POST.get('city'),
                              street=request.POST.get('street'),
                              street_number=request.POST.get('street_number'),
                              postcode=request.POST.get('postcode'),
                              suite_number=request.POST.get('suite_number'),
                              email=request.POST.get('email'),
                              social_links=request.POST.get('social_links'),
                              logo=request.FILES['logo'],
                              phone=request.POST.get('phone'),
                              user=User.objects.get(pk=request.user.pk)
                              )
            company.save()
            return redirect('home')

    else:
        form = CreateCompanyForm()

    context = {'form': form}
    return render(request, 'Index/register_company.html', context)


def applyForJob(request, *args, **kwargs):
    if request.method == "POST":
        form = CreateApplicationForm(request.POST, request.FILES)
        offer_id = kwargs['offer_id']
        if form.is_valid():
            application = Application(first_name=request.POST.get('first_name'),
                                      last_name=request.POST.get('last_name'),
                                      email=request.POST.get('email'),
                                      cv=request.FILES['cv'],
                                      reason=request.POST.get('reason'),
                                      offer=get_object_or_404(Offer, pk=offer_id)
                                      )
            application.save()
            return redirect('home')

    else:
        form = CreateApplicationForm()

    context = {'form': form, 'offer_id': kwargs['offer_id']}
    return render(request, "Offers/apply-for-job.html", context)


def jobs(request):
    offersList = Offer.objects.all()
    return render(request, "Offers/jobs.html", {'offers_list': offersList})


def job_details(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    company = get_object_or_404(Company, pk=offer.company_id)
    return render(request, 'Offers/job-details.html', {'offer': offer, 'company': company})
