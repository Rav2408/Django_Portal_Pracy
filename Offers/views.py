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

                    user = authenticate(username=username, password=password)
                    login(request, user)
                else:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                    return redirect('register')

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
    company = get_object_or_404(Company, user=request.user.pk)
    offer_list = Offer.objects.filter(company=company)
    application_list = []
    application_count = {}
    for i in offer_list:
        application_list = Application.objects.all().filter(offer_id=i.id)
        application_count[i.id] = Application.objects.filter(offer_id=i.id).count()
    return render(request, 'Index/profile.html', {'company': company, 'offers_lists': offer_list,
                                                  'application_count': application_count,
                                                  'application_list': application_list})


def addoffer(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateOfferForm(request.POST)
            if form.is_valid():
                offer = Offer(company=get_object_or_404(Company, user=request.user.pk),
                              position=form.cleaned_data['position'],
                              min_salary=form.cleaned_data['min_salary'],
                              max_salary=form.cleaned_data['max_salary'],
                              remote=form.cleaned_data['remote'],
                              location=form.cleaned_data['location'],
                              description=form.cleaned_data['description']
                              )

                offer.save()
                return redirect('home')

        else:
            form = CreateOfferForm()

    context = {'form': form}
    return render(request, "Index/addoffer.html", context)


def registerCompany(request, *args, **kwargs):

    if request.method == "POST":
        form = CreateCompanyForm(request.POST, request.FILES)
        messages.success(request, 'Account was created!')
        if form.is_valid():
            logo = None
            if request.FILES:
                logo = request.FILES['logo']
            company = Company(company_name=form.cleaned_data['company_name'],
                              city=form.cleaned_data['city'],
                              street=form.cleaned_data['street'],
                              street_number=form.cleaned_data['street_number'],
                              postcode=form.cleaned_data['postcode'],
                              suite_number=form.cleaned_data['suite_number'],
                              email=form.cleaned_data['email'],
                              social_links=form.cleaned_data['social_links'],
                              logo=logo,
                              phone=form.cleaned_data['phone'],
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
            application = Application(first_name=form.cleaned_data['first_name'],
                                      last_name=form.cleaned_data['last_name'],
                                      email=form.cleaned_data['email'],
                                      cv=request.FILES['cv'],
                                      reason=form.cleaned_data['reason'],
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
    #trzeba stworzyć tu słownik ofert z ich zdjęciami
    logo_dict = {}
    for offer in offersList:
        company = get_object_or_404(Company, pk = offer.company_id)
        logo_dict[offer] = company.logo
    return render(request, "Offers/jobs.html", {'offers_list': offersList, 'logo_dict': logo_dict})


def job_details(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    company = get_object_or_404(Company, pk=offer.company_id)
    return render(request, 'Offers/job-details.html', {'offer': offer, 'company': company})
