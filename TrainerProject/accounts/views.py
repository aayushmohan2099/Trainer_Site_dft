from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import (
    BeneficiaryRegistrationForm, BeneficiaryProfileForm,
    MasterTrainerRegistrationForm, MasterTrainerProfileForm, UserUpdateForm,VOUserEditForm,
)

from django.contrib.auth.views import LoginView, LogoutView

from .models import Beneficiary, MasterTrainer, VillageOrganizer

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import Beneficiary, VillageOrganizer
from django.contrib.admin.views.decorators import staff_member_required

from django.views.decorators.cache import never_cache

from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import SetPasswordForm


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

@never_cache
@login_required
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

@never_cache
@login_required
def trainer_home(request):
    return render(request, 'accounts/trainer_home.html')

# Site login based on whether they are Beneficiary or MasterTrainer
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        u = self.request.user
        if hasattr(u, 'beneficiary'):     return '/accounts/beneficiary/home/'
        if hasattr(u, 'mastertrainer'):   return '/accounts/trainer/home/'
        if hasattr(u, 'villageorganizer'):return '/accounts/vo/dashboard/'
        return '/'

class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        # Treating GET like POST for csrf security reasons
        return self.post(request, *args, **kwargs)
        
@never_cache
@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        if hasattr(user, 'beneficiary'):   return redirect('beneficiary_home')
        if hasattr(user, 'mastertrainer'): return redirect('trainer_home')
        if hasattr(user, 'villageorganizer'): return redirect('vo_dashboard')
        return redirect('login')
    return render(request, 'accounts/change_password.html', {'form': form})

#  VO Dashboard
@never_cache
@login_required
def vo_dashboard(request):
    if not hasattr(request.user, 'villageorganizer'):
            return redirect('login')
    vo = request.user.villageorganizer
    beneficiaries = Beneficiary.objects.select_related('user').filter(village=vo.village)
    return render(request, 'accounts/vo_dashboard.html', {'beneficiaries': beneficiaries})

# VO editing beneficiaries
@login_required
@never_cache
def vo_edit_beneficiary(request, pk):
    # Only VOs can edit beneficiaries of their village
    if not hasattr(request.user, 'villageorganizer'):
        return redirect('login')
    vo_village = request.user.villageorganizer.village

    b = get_object_or_404(Beneficiary.objects.select_related('user'), pk=pk, village=vo_village)
    user_form = VOUserEditForm(request.POST or None, instance=b.user)
    pwd_form = SetPasswordForm(b.user, request.POST or None)

    if request.method == "POST":
        ok1 = user_form.is_valid()
        ok2 = ('new_password1' in request.POST) and pwd_form.is_valid()
        if ok1:
            user_form.save()
        if ok2:
            pwd_form.save()
            # update demo temp password field so export shows the latest
            b.temp_password = request.POST.get('new_password1') or b.temp_password
            b.save(update_fields=['temp_password'])
        if ok1 or ok2:
            return redirect('vo_dashboard')

    return render(request, 'accounts/vo_edit_beneficiary.html', {'b': b, 'user_form': user_form, 'pwd_form': pwd_form})

# For editing Profiles after login
@login_required
@never_cache
def edit_profile(request):
    user_form = UserUpdateForm(request.POST or None, instance=request.user)

    # Pick the right profile form if user has one
    profile_form = None
    if hasattr(request.user, "beneficiary"):
        profile_form = BeneficiaryProfileForm(request.POST or None, instance=request.user.beneficiary)
    elif hasattr(request.user, "mastertrainer"):
        profile_form = MasterTrainerProfileForm(request.POST or None, instance=request.user.mastertrainer)

    if request.method == "POST" and user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
        user_form.save()
        if profile_form:
            profile_form.save()
        # send them back to their home
        if hasattr(request.user, "beneficiary"):
            return redirect("beneficiary_home")
        if hasattr(request.user, "mastertrainer"):
            return redirect("trainer_home")
        if hasattr(request.user, "villageorganizer"):
            return redirect("vo_dashboard")
        return redirect("login")
    return render(request, "accounts/edit_profile.html", {"user_form": user_form, "profile_form": profile_form})


