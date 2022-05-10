from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Offer
from .forms import OrderForm, CreateUserForm
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, "Offers/base.html", {})


#def user_login(request):
#    return render(request, "registration/login.html", {})

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


def home(request):
    return render(request, "Index/index.html", {})


def about(request):
    return render(request, "Index/about.html", {})


def jobs(request):
    offersList = Offer.objects.all()
    return render(request, "Offers/jobs.html", {'offers_list':offersList})

def job_details(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'Offers/job-details.html', {'offer': offer})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                messages.success(request, 'Account was created for ' + username)

                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')

        context = {'form': form}
        return render(request, 'registration/register.html', context)

#def register(request):

  #  if request.method == 'POST':
   #     form = CreateUserForm(request.POST)
    #    if form.is_valid():
     #       form.save()
      #      username = form.cleaned_data.get('username')
       #     password = form.cleaned_data['password1']
       #     user = authenticate(username=username, password=password)
       #     login(request, user)
       #     return redirect('home')
    #else:
    #    form = UserCreationForm()

   # context = {'form': form}
   # return render(request, 'registration/register.html', context)


def logout_view(request):
    logout(request)
    return render(request, "Index/index.html", {})


def logout_view(request):
    logout(request)
    return render(request, "Index/index.html", {})


#/offer_id wyświetla stronę ze szczegółami na temat tej oferty
def detail(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'Offers/detail.html', {'offer': offer})


#tworzysz zmienną przechowującą liste obiektów a następnie
#przekazujesz ją do pliku HTML pod nazwą zadeklarowaną w cudzysłowach (3 parametr render)
def offers_list(request):
    offersList = Offer.objects.all()
    return render(request, 'Offers/offers_list.html', {'offers_list':offersList})