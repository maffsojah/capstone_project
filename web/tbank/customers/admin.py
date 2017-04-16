from django.contrib import admin

from . import models


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_balance</i>'
    list_display = ('service_no', 'service_name', 'service_description')

@admin.register(models.ServiceCustomer)
class ServiceCustomerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">people_outline</i>'
    list_display = ('customer', 'service', 'from_date', 'to_date')
    list_select_related = True
    raw_id_fields = ('customer', )
    list_filter = ('service', )
    list_per_page = 10

# @admin.register(models.ServiceManager)
# class ServiceManagerAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">assignment_ind</i>'
#     list_display = ('customer', 'service', 'from_date', 'to_date')
#     raw_id_fields = ('customer', )
#     list_filter = ('service', )

## Custom Action for the customers
def all_customers(ModelAdmin, request, queryset):
    for qs in queryset:
        print qs.Name

# def allocated_services(ModelAdmin, request, queryset):
#     queryset.update()

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_box</i>'
    list_display = ('Customer_ID', 'Name', 'Gender', 'Nationality', 'Account_Type', 'Balance')
    list_per_page = 10
    list_filter = ('Nationality', 'Gender')
    actions = [all_customers]

@admin.register(models.Salary)
class SalaryAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_balance_wallet</i>'
    list_display = ('customer', 'from_date', 'to_date', 'salary')
    raw_id_fields = ('customer', )

# @admin.register(models.Title)
# class TitleAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">reorder</i>'
#     list_display = ('customer', 'from_date', 'to_date', 'title')
#     raw_id_fields = ('customer', )
#     list_filter = ('title', )
