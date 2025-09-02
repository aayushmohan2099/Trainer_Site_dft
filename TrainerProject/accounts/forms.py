from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Beneficiary, MasterTrainer

# Beneficiary Login Registration (User Creation)
class BeneficiaryRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Beneficiary Profile Creations
class BeneficiaryProfileForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = [
            'state', 'district', 'block', 'gram_panchayat', 'village',
            'shg_code', 'shg_name', 'member_code', 'member_name',
            'marital_status', 'disability_status', 'bank_account_no', 'ifsc_code'
        ]

# Trainer Login Registration (User Creation)
class MasterTrainerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Trainer Profile creation
class MasterTrainerProfileForm(forms.ModelForm):
    class Meta:
        model = MasterTrainer
        fields = ['full_name', 'qualification', 'expertise', 'training_history', 'availability']
