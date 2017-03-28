from django.contrib import admin
from .models import Service, Level

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    model = Service
    list_display = ('Customer_ID', 'Name', 'Gender', 'Address', 'Nationality', 'Account_Type', 'Age', 'Education', 'Employment', 'Salary',
                    'Employer_Stability', 'Customer_Loyalty', 'Balance', 'Residential_Status', 'Service_Level')
    list_filter = ['Name', 'Service_Level', 'Account_Type', 'Gender', 'Customer_ID']
    search_fields = ['Balance', 'Nationality']

admin.site.register(Level)
admin.site.register(Service, ServiceAdmin)
