from django import forms
from django.contrib import admin
from django.db import models as django
from django.utils.text import Truncator
from django.utils.html import mark_safe, format_html


from . import models



# Register your models here.

# class CustomerTabularInline(admin.TabularInline):
#     #fields = ('Name', 'Service_Level' )
#     model = models.Customer
#
#     # class CustomerInlineFormset(forms.models.BaseInlineFormSet):
#     #     def clean(self):
#     #         super(CustomerTabularInline.CustomerInlineFormset, self).clean()
#     #         if not hasattr(self, 'cleaned_data'):
#     #             return
#     #
#     #         for form_data in self.cleaned_data:
#     #             Service_Level = form_data.get('Service_Level', None)
#     #             if Service_Level and len(Service_Level) > 2:
#     #                 raise forms.ValidationError('The customer has used bank for less than a year and is not suitable for T-Bank Services')
#     #             return self.cleaned_data
#     #
#     # formset = CustomerInlineFormset
#
#     def has_add_permission(self, request):
#         return False

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">perm_identity</i>'

    # fieldsets = (
    #     (None, {
    #         'fields': ('Name',)}),
    #     ('Customer Personal Details', {
    #         'fields': ('Gender', 'Age', ('Address', 'Nationality'),
    #                     ('Education', 'Residential_Status', 'Employment'))}),
    #     ('Customer Bank Details', {
    #         'fields': ('Account_Type', 'Service_Level',
    #                     ('Employer_Stability', 'Customer_Loyalty', 'Balance', 'Salary'))})
    # )

#    inlines = [CustomerTabularInline]

    # list_display = ('Customer_ID', 'Name', 'Gender', 'Address', 'Nationality', 'Account_Type', 'Age', 'Education', 'Employment', 'Salary',
    #                 'Employer_Stability', 'Customer_Loyalty', 'Balance', 'Residential_Status', 'Service_Level')
    list_display = ('Customer_ID', 'Name', 'Gender', 'Nationality', 'Account_Type', 'Age', 'Salary', 'Service_Level')
    # list_filter = ['Name', 'Service_Level', 'Account_Type', 'Gender']
    # ordering = ['Gender', 'Age', 'Service_Level', 'Nationality', 'Education', 'Employment', 'Residential_Status']

    search_fields = ['Balance', 'Nationality']

@admin.register(models.ServiceLevel)
class ServiceAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">redeem</i>'
    list_display = ('service_name','description', 'pub_date')
    list_filter = ['service_name']
    search_fields = ['service_name']

# @admin.register(models.CustomerLoyalty)
# class LoyaltyAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">loyalty</i>'
#     list_display = ['customer_loyalty']
