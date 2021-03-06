import json
import urllib
import urllib.parse
import urllib.request
import os
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from Django_Portal_Pracy.settings import MEDIA_ROOT
from django.core.files.storage import FileSystemStorage

from django.views.generic import ListView, DetailView, CreateView

from django.core.paginator import Paginator
import Offers
from Django_Portal_Pracy import settings
from .models import Offer, Company, Application
from .forms import CreateUserForm, CreateOfferForm, CreateCompanyForm, CreateApplicationForm, UpdateUserForm
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
                messages.error(request, 'The data entered is incorrect. '
                                        'Make sure that the password is at least 8 characters long')

        else:
            form = CreateUserForm()  # to ta z polem emaila

        form = CreateUserForm()  # to ta z polem emaila
        context = {'form': form}
        return render(request, 'registration/register.html', context)


def edit_user(request):
    instance = request.user
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=instance)
        if form.is_valid():
            instance.username = form.cleaned_data.get('username')
            instance.set_password(form.cleaned_data.get('password'))
            instance.email = form.cleaned_data.get('email')
            instance.save(update_fields=['username', 'password', 'email'])

            user = authenticate(username=instance.username, password=instance.password)
            login(request, user)

            return redirect('profile')
    else:
        form = UpdateUserForm(instance=instance)

    context = {'form': form}
    return render(request, 'Index/edit_user.html', context)


def home(request):
    return render(request, "Index/index.html", {})


def error(request):
    return render(request, "Index/error.html", {})


def profile(request):
    company = get_object_or_404(Company, user=request.user.pk)
    user = user = request.user

    return render(request, 'Index/profile.html', {'company': company, 'user': user})


def company_profile(request):
    company = get_object_or_404(Company, user=request.user.pk)
    offer_list = Offer.objects.filter(company=company)
    application_list = []
    application_count = {}
    for i in offer_list:
        list = Application.objects.all().filter(offer_id=i.id)
        for app in list:
            application_list.append(app)
        application_count[i.id] = Application.objects.filter(offer_id=i.id).count()
    return render(request, 'Index/company_profile.html', {'company': company, 'offers_lists': offer_list,
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


def edit_company(request, *args, **kwargs):
    instance = Company.objects.get(user=request.user.pk)
    if request.method == "POST":
        logo = instance.logo
        if request.FILES:
            if logo:
                if os.path.exists(os.path.join(MEDIA_ROOT, logo.name)):
                    os.remove(os.path.join(MEDIA_ROOT, logo.name))
        form = CreateCompanyForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            logo = request.FILES['logo']
            instance.company_name = form.cleaned_data['company_name']
            instance.city = form.cleaned_data['city']
            instance.street = form.cleaned_data['street']
            instance.street_number = form.cleaned_data['street_number']
            instance.postcode = form.cleaned_data['postcode']
            instance.suite_number = form.cleaned_data['suite_number']
            instance.email = form.cleaned_data['email']
            instance.social_links = form.cleaned_data['social_links']
            instance.logo = logo
            instance.phone = form.cleaned_data['phone']
            instance.save(update_fields=['company_name',
                                         'city',
                                         'street',
                                         'street_number',
                                         'postcode',
                                         'suite_number',
                                         'email',
                                         'social_links',
                                         'logo',
                                         'phone'])

            return redirect('profile')
    else:
        form = CreateCompanyForm(instance=instance)

    context = {'form': form}
    return render(request, 'Index/edit_company.html', context)


def edit_offer(request, id):
    instance = Offer.objects.get(id=id)
    if request.method == "POST":
        form = CreateOfferForm(request.POST, instance=instance)
        if form.is_valid():
            instance.position = form.cleaned_data['position']
            instance.min_salary = form.cleaned_data['min_salary']
            instance.max_salary = form.cleaned_data['max_salary']
            instance.remote = form.cleaned_data['remote']
            instance.location = form.cleaned_data['location']
            instance.description = form.cleaned_data['description']
            instance.save(update_fields=['position',
                                         'min_salary',
                                         'max_salary',
                                         'remote',
                                         'location',
                                         'description'])

            return redirect('company_profile')
    else:
        form = CreateOfferForm(instance=instance)
    context = {'form': form, 'id': id}
    return render(request, 'Index/edit_offer.html', context)


def applyForJob(request, *args, **kwargs):
    if request.method == "POST":
        form = CreateApplicationForm(request.POST, request.FILES)
        offer_id = kwargs['offer_id']
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
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                form = CreateApplicationForm()
        else:
            messages.error(request, 'Invalid CV file')
    form = CreateApplicationForm()
    context = {'form': form, 'offer_id': kwargs['offer_id']}
    return render(request, "Offers/apply-for-job.html", context)


def jobs(request):
    offersList = Offer.objects.all()

    pagination = Paginator(Offer.objects.all(), 10)
    page = request.GET.get('page')
    j = pagination.get_page(page)  # j jak jobs

    # s??ownik ofert z zdj??ciami ich firm
    logo_dict = {}
    for offer in offersList:
        company = get_object_or_404(Company, pk=offer.company_id)
        logo_dict[offer] = company.logo
    return render(request, "Offers/jobs.html", {'offers_list': offersList,
                                                'offers_list2': j,
                                                'logo_dict': logo_dict})


def job_details(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    company = get_object_or_404(Company, pk=offer.company_id)
    return render(request, 'Offers/job-details.html', {'offer': offer, 'company': company})


def delete_application(request, id):
    ob = Application.objects.get(id=id)
    ob.delete()
    return redirect('company_profile')


def delete_offer(request, id):
    ob = Offer.objects.get(id=id)
    ob.delete()
    return redirect('company_profile')


def is_valid_query(param):
    return param != '' and param is not None


def search(request):
    offers = Offer.objects.all()

    min_pay = request.GET.get('min_pay_html')
    max_pay = request.GET.get('max_pay_html')

    position = request.GET.get('position_html')
    company = request.GET.get('company_html')

    location = request.GET.get('location_html')

    remote = request.GET.get('remote_html')
    context = {}

    if is_valid_query(min_pay):
        offers = offers.filter(min_salary__gte=min_pay)  # gte - greater than or equal
        context['min_pay'] = min_pay

    if is_valid_query(max_pay):
        offers = offers.filter(max_salary__lte=max_pay)  # lower than or equal
        context['max_pay'] = max_pay

    if is_valid_query(position):
        offers = offers.filter(position__icontains=position)
        context['position'] = position

    if is_valid_query(company):
        offers = offers.filter(company__company_name__icontains=company)
        # foreign key - field - lookup
        context['company'] = company

    if is_valid_query(location):
        offers = offers.filter(location__icontains=location)
        context['location'] = location

    if remote == 'on':
        offers = offers.filter(remote=True)
        context['remote'] = remote

    logo_dict = {}
    for offer in offers:
        company = get_object_or_404(Company, pk=offer.company_id)
        logo_dict[offer] = company.logo

    context['result'] = offers
    context['logo_dict'] = logo_dict

    return render(request, 'Offers/search.html', context)

def error_404(request, exception):
    data = {}
    return render(request, 'Index/error.html', data)

