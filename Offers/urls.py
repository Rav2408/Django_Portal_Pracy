from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("register/", views.user_register, name='register'),
    path("logout/", views.logout_view, name='logout_view'),
    path('<int:offer_id>/', views.detail, name='detail'),
    path('offers_list/', views.offers_list, name='offers_list'),
    path('jobs/', views.jobs, name='jobs'),
    path('login/', views.user_login, name='login'),
    path('about/', views.about, name='about')
]