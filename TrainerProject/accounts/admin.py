from django.contrib import admin

from .models import Beneficiary, MasterTrainer

from django import forms
from django.shortcuts import render, redirect
from django.urls import path
import openpyxl

admin.site.register(Beneficiary)
admin.site.register(MasterTrainer)

# Excel -> DB Upload Form
class ExcelUploadForm(forms.Form):
    file = forms.FileField()


# Custom Admin Portal for Import/Export of Bulk Data
class CustomAdminSite(admin.AdminSite):
    site_header = "Training Management Admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.admin_view(self.upload_excel), name='upload_excel'),
        ]
        return custom_urls + urls

    def upload_excel(self, request):
        if request.method == "POST":
            form = ExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                wb = openpyxl.load_workbook(form.cleaned_data['file'])
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if row[0] == "Beneficiary":
                        Beneficiary.objects.create(
                            user_id=row[1], state=row[2], district=row[3],
                            block=row[4], gram_panchayat=row[5], village=row[6],
                            shg_code=row[7], shg_name=row[8], member_code=row[9],
                            member_name=row[10], marital_status=row[11],
                            disability_status=row[12], bank_account_no=row[13],
                            ifsc_code=row[14]
                        )
                    elif row[0] == "Trainer":
                        MasterTrainer.objects.create(
                            user_id=row[1], full_name=row[2],
                            qualification=row[3], expertise=row[4],
                            training_history=row[5], availability=row[6]
                        )
                return redirect("..")
        else:
            form = ExcelUploadForm()
        return render(request, "admin/upload_excel.html", {"form": form})
