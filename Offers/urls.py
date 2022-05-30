from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("register/", views.user_register, name='register'),
    path("logout/", views.logout_view, name='logout_view'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/job-details/<int:offer_id>/', views.job_details, name='job-details'),
    path('jobs/job-details/<int:offer_id>/apply-for-job', views.applyForJob, name='apply-for-job'),
    path('login/', views.user_login, name='login'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('register_company/', login_required(views.registerCompany), name='register_company')
]