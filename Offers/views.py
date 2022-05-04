from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Offer
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, "Offers/base.html", {})


def login(request):
    return render(request, "registration/login.html", {})


def home(request):
    return render(request, "Index/index.html", {})


def jobs(request):
    return render(request, "Offers/jobs.html", {})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    context = {'form' : form }
    return render(request, 'registration/register.html', context)


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