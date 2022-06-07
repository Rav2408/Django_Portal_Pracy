from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='home'),
    path("register/", views.user_register, name='register'),
    path("error/", views.error, name='error'),
    path("logout/", views.logout_view, name='logout_view'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/job-details/<int:offer_id>/', views.job_details, name='job-details'),
    path('jobs/job-details/<int:offer_id>/apply-for-job', views.applyForJob, name='apply-for-job'),
    path('login/', views.user_login, name='login'),
    path('company_profile/', views.company_profile, name='company_profile'),
    path('profile/', views.profile, name='profile'),
    path('register_company/', login_required(views.registerCompany), name='register_company'),
    path('edit_company/', login_required(views.edit_company), name='edit_company'),
    path('edit_user/', login_required(views.edit_user), name='edit_user'),
    path('company_profile/edit_offer/<int:id>/', login_required(views.edit_offer), name='edit_offer'),
    path('addoffer/', login_required(views.addoffer), name='addoffer'),
    path('application-delete/<int:id>', views.delete_application, name='application_delete'),
    path('offer-delete/<int:id>', views.delete_offer, name='offer_delete'),
    path('jobs/search/', views.search, name='search'),
    path('jobs/search/job-details/<int:offer_id>/', views.job_details, name='job-details'),
    path('jobs/search/job-details/<int:offer_id>/apply-for-job', views.applyForJob, name='apply-for-job')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

