from django.contrib import admin
from django.contrib.messages import SUCCESS
import csv
from django.http import HttpResponse
from django.db.models import Case, Value, When

from . import models
from models import Customer, Service


## Custom Action for the customers
def allocate_service(ModelAdmin, request, queryset):
    platinum_customers = []
    silver_customers = []
    message = ''

    for customer in queryset:
        if customer.Salary >= 10000 and customer.Residential_Status == 'Owned' and customer.Employer_Stability == 'Stable':
            # customer.Service_Level = 'Platinum Package'
            customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
            platinum_customers.append(customer.Name)
        elif customer.Salary <= 1000 and customer.Residential_Status == 'Rented' and customer.Employer_Stability == 'Unstable':
            # customer.Service_Level = 'Silver Package'
            customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
            silver_customers.append(customer.Name)
        customer.save()

        if platinum_customers:
            message = 'The following customers are now platinum: {}'.format(', '.join(platinum_customers))
        if silver_customers:
            message = 'The following customers are now silver: {}'.format(', '.join(silver_customers))
        if not platinum_customers and not silver_customers:
            message = 'No customer changes!'
        ModelAdmin.message_user(request, message, level=SUCCESS)
allocate_service.short_description = 'Allocate Service'


def export_customers(ModelAdmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Customer_ID', 'Name', 'Gender','Age', 'Nationality', 'Address', 'Account_Type', 'Salary', 'Balance', 'Employer_Stability', 'Customer_Loyalty', 'Residential_Status', 'Service_Level'])
    customers = queryset.values_list('Customer_ID', 'Name', 'Gender','Age', 'Nationality', 'Address', 'Account_Type', 'Salary', 'Balance', 'Employer_Stability', 'Customer_Loyalty', 'Residential_Status', 'Service_Level')
    for customer in customers:
        writer.writerow(customer)
    return response
export_customers.short_description = 'Export to csv'

# class CustomerInline(admin.TabularInline):
#     model = Customer


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_balance</i>'
    list_display = ( 'service_name', 'service_description') # 'service_no',

@admin.register(models.ServiceCustomer)
class ServiceCustomerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">people_outline</i>'
    list_display = ('customer', 'service', 'from_date', 'to_date')
    list_select_related = True
    raw_id_fields = ('customer', )
    list_filter = ('service', )
    list_per_page = 10
    # inlines = [
    #     CustomerInline,
    # ]

# @admin.register(models.ServiceManager)
# class ServiceManagerAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">assignment_ind</i>'
#     list_display = ('customer', 'service', 'from_date', 'to_date')
#     raw_id_fields = ('customer', )
#     list_filter = ('service', )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_box</i>'
    list_display = ('Customer_ID', 'Name', 'Gender', 'Nationality', 'Account_Type', 'Salary', 'Balance', 'Service_Level')
    list_per_page = 10
    list_filter = ('Nationality', 'Gender')
    actions = [export_customers, allocate_service,]


# @admin.register(models.Salary)
# class SalaryAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">account_balance_wallet</i>'
#     list_display = ('customer', 'from_date', 'to_date', 'salary')
#     raw_id_fields = ('customer', )

# @admin.register(models.Title)
# class TitleAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">reorder</i>'
#     list_display = ('customer', 'from_date', 'to_date', 'title')
#     raw_id_fields = ('customer', )
#     list_filter = ('title', )
