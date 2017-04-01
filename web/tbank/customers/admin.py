from django.contrib import admin

from . import models


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_balance</i>'
    list_display = ('service_no', 'service_name', 'service_description')


@admin.register(models.ServiceEmployee)
class ServiceEmployeeAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">people_outline</i>'
    list_display = ('employee', 'service', 'from_date', 'to_date')
    list_select_related = True
    raw_id_fields = ('employee', )
    list_filter = ('service', )


@admin.register(models.ServiceManager)
class ServiceManagerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">assignment_ind</i>'
    list_display = ('employee', 'service', 'from_date', 'to_date')
    raw_id_fields = ('employee', )
    list_filter = ('service', )


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_box</i>'
    list_display = ('Customer_ID', 'Name', 'Gender', 'Nationality', 'Account_Type', 'Salary')


@admin.register(models.Salary)
class SalaryAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_balance_wallet</i>'
    list_display = ('employee', 'from_date', 'to_date', 'salary')
    raw_id_fields = ('employee', )


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">reorder</i>'
    list_display = ('employee', 'from_date', 'to_date', 'title')
    raw_id_fields = ('employee', )
    list_filter = ('title', )
