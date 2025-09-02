from django.urls import path
from . import views

urlpatterns = [
    path('beneficiary/register/', views.beneficiary_register, name='beneficiary_register'),
    path('beneficiary/home/', views.beneficiary_home, name='beneficiary_home'),
    path('trainer/register/', views.trainer_register, name='trainer_register'),
    path('trainer/home/', views.trainer_home, name='trainer_home'),
]
