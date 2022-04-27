from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name='home'),
    path("", views.home, name='home'),
    path("register/", views.register, name='register'),
    path("logout/", views.logout_view, name='logout_view'),

]