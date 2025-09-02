from django.contrib import admin

from .models import Beneficiary, MasterTrainer

from django import forms
from django.shortcuts import render, redirect
from django.urls import path
import openpyxl

from django.http import HttpResponse

# Excel -> DB Upload Form
class ExcelUploadForm(forms.Form):
    file = forms.FileField()


# Custom Admin Portal for Import/Export of Bulk Data

# Beneficiary Data
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'shg_name', 'village', 'marital_status')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel), name="beneficiary_import_excel"),
            path('export-excel/', self.admin_site.admin_view(self.export_excel), name="beneficiary_export_excel"),
        ]
        return custom_urls + urls

    def import_excel(self, request):
        if request.method == "POST":
            form = ExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                wb = openpyxl.load_workbook(form.cleaned_data['file'])
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    Beneficiary.objects.create(
                        user_id=row[1], state=row[2], district=row[3],
                        block=row[4], gram_panchayat=row[5], village=row[6],
                        shg_code=row[7], shg_name=row[8], member_code=row[9],
                        member_name=row[10], marital_status=row[11],
                        disability_status=row[12], bank_account_no=row[13],
                        ifsc_code=row[14]
                    )
                self.message_user(request, "Beneficiaries imported successfully!")
                return redirect("..")
        else:
            form = ExcelUploadForm()
        return render(request, "admin/upload_excel.html", {"form": form, "title": "Import Beneficiaries"})

    def export_excel(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Beneficiaries"
        ws.append(["UserID", "State", "District", "Block", "GP", "Village",
                   "SHG Code", "SHG Name", "Member Code", "Member Name",
                   "Marital Status", "Disability", "Bank Account", "IFSC Code"])
        for b in Beneficiary.objects.all():
            ws.append([
                b.user.id, b.state, b.district, b.block, b.gram_panchayat, b.village,
                b.shg_code, b.shg_name, b.member_code, b.member_name,
                b.marital_status, b.disability_status, b.bank_account_no, b.ifsc_code
            ])
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="beneficiaries.xlsx"'
        wb.save(response)
        return response

# Download format for data input
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel), name="beneficiary_import_excel"),
            path('export-excel/', self.admin_site.admin_view(self.export_excel), name="beneficiary_export_excel"),
            path('download-format/', self.admin_site.admin_view(self.download_format), name="beneficiary_download_format"),
        ]
        return custom_urls + urls

    def download_format(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Beneficiaries"
        ws.append(["UserID", "State", "District", "Block", "GP", "Village",
                "SHG Code", "SHG Name", "Member Code", "Member Name",
                "Marital Status", "Disability", "Bank Account", "IFSC Code"])
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="beneficiary_format.xlsx"'
        wb.save(response)
        return response

# Master Trainer Data
class MasterTrainerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'qualification', 'availability')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel), name="trainer_import_excel"),
            path('export-excel/', self.admin_site.admin_view(self.export_excel), name="trainer_export_excel"),
        ]
        return custom_urls + urls

    def import_excel(self, request):
        if request.method == "POST":
            form = ExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                wb = openpyxl.load_workbook(form.cleaned_data['file'])
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    MasterTrainer.objects.create(
                        user_id=row[1], full_name=row[2],
                        qualification=row[3], expertise=row[4],
                        training_history=row[5], availability=row[6]
                    )
                self.message_user(request, "Trainers imported successfully!")
                return redirect("..")
        else:
            form = ExcelUploadForm()
        return render(request, "admin/upload_excel.html", {"form": form, "title": "Import Trainers"})

    def export_excel(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Trainers"
        ws.append(["UserID", "Full Name", "Qualification", "Expertise", "Training History", "Availability"])
        for t in MasterTrainer.objects.all():
            ws.append([
                t.user.id, t.full_name, t.qualification, t.expertise,
                t.training_history, t.availability
            ])
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="trainers.xlsx"'
        wb.save(response)
        return response

# For bulk data input format download
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel), name="trainer_import_excel"),
            path('export-excel/', self.admin_site.admin_view(self.export_excel), name="trainer_export_excel"),
            path('download-format/', self.admin_site.admin_view(self.download_format), name="trainer_download_format"),
        ]
        return custom_urls + urls

    def download_format(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Trainers"
        ws.append(["UserID", "Full Name", "Qualification", "Expertise", "Training History", "Availability"])
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="trainer_format.xlsx"'
        wb.save(response)
        return response
    

admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(MasterTrainer, MasterTrainerAdmin)