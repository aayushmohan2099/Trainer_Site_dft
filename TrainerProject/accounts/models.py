from django.db import models

from django.contrib.auth.models import User


# Beneficiary | Sakhi Model
class Beneficiary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Geographic Data
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    block = models.CharField(max_length=100)
    gram_panchayat = models.CharField(max_length=100)
    village = models.CharField(max_length=100)

    # Membership Info
    shg_code = models.CharField(max_length=50)
    shg_name = models.CharField(max_length=200)
    member_code = models.CharField(max_length=50)
    member_name = models.CharField(max_length=200)

    # Dates
    registration_date = models.DateField(auto_now_add=True)

    # Demographics & Finance
    marital_status = models.CharField(max_length=50, choices=[
        ('Unmarried', 'Unmarried'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed')
    ])
    disability_status = models.BooleanField(default=False)
    bank_account_no = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)

    temp_password = models.CharField(max_length=64, blank=True, null=True)  # demo only!

    def __str__(self):
        return f"{self.member_name} ({self.shg_name})"


# Master Trainer Model
class MasterTrainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    expertise = models.TextField()
    training_history = models.TextField(blank=True, null=True)
    availability = models.CharField(max_length=200, help_text="e.g. Weekdays, Weekends")

    temp_password = models.CharField(max_length=64, blank=True, null=True)  # demo only!

    def __str__(self):
        return self.full_name
    

#  Village Organizer (VO) model
class VillageOrganizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    village = models.CharField(max_length=100)

    def __str__(self):
        return f"VO {self.user.username} - {self.village}"


