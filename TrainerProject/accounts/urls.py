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
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('vo/dashboard/', views.vo_dashboard, name='vo_dashboard'),
    path('vo/beneficiary/<int:pk>/edit/', views.vo_edit_beneficiary, name='vo_edit_beneficiary'),
]
