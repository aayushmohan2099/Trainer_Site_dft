from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import (
    BeneficiaryRegistrationForm, BeneficiaryProfileForm,
    MasterTrainerRegistrationForm, MasterTrainerProfileForm
)


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
