from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import (
    BeneficiaryRegistrationForm, BeneficiaryProfileForm,
    MasterTrainerRegistrationForm, MasterTrainerProfileForm
)

from django.contrib.auth.views import LoginView, LogoutView

from .models import Beneficiary, MasterTrainer

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Beneficiary User/Profile Creation ModelView
def beneficiary_register(request):
    if request.method == 'POST':
        user_form = BeneficiaryRegistrationForm(request.POST)
        profile_form = BeneficiaryProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('beneficiary_home')
    else:
        user_form = BeneficiaryRegistrationForm()
        profile_form = BeneficiaryProfileForm()
    return render(request, 'accounts/beneficiary_register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def beneficiary_home(request):
    return render(request, 'accounts/beneficiary_home.html')


# Master Trainer User/Profile Creation ModelView
def trainer_register(request):
    if request.method == 'POST':
        user_form = MasterTrainerRegistrationForm(request.POST)
        profile_form = MasterTrainerProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('trainer_home')
    else:
        user_form = MasterTrainerRegistrationForm()
        profile_form = MasterTrainerProfileForm()
    return render(request, 'accounts/trainer_register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def trainer_home(request):
    return render(request, 'accounts/trainer_home.html')

# Site login based on whether they are Beneficiary or MasterTrainer
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        # Check role and redirect
        if hasattr(user, 'beneficiary'):
            return '/accounts/beneficiary/home/'
        elif hasattr(user, 'mastertrainer'):
            return '/accounts/trainer/home/'
        else:
            return '/'  # fallback
        
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep logged in
            return redirect('beneficiary_home')  # or trainer_home
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})