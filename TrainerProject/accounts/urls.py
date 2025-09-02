from django.urls import path
from . import views

from .views import UserLoginView, UserLogoutView

urlpatterns = [
    path('beneficiary/register/', views.beneficiary_register, name='beneficiary_register'),
    path('beneficiary/home/', views.beneficiary_home, name='beneficiary_home'),
    path('trainer/register/', views.trainer_register, name='trainer_register'),
    path('trainer/home/', views.trainer_home, name='trainer_home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change-password/', views.change_password, name='change_password'),
]
