from django.contrib import admin
from django.contrib.messages import SUCCESS
import csv
from django.http import HttpResponse
from django.db.models import Case, Value, When
from django.db import connection
import operator
import inspect

import pandas as pd
import numpy as np
from django_pandas.io import read_frame

from . import models
from models import Customer, Service

#####  PLAN B ALLOCATION


def allocate_service(ModelAdmin, request, queryset):
    platinum_customers = []
    silver_customers = []
    gold_customers = []
    non_customers = []
    message = ''



    for customer in queryset:
        qs = Customer.objects.all()
        df = qs.to_dataframe(fieldnames=["Age","Education", "Employment", "Employer_Stability", "Residential_Status", "Salary", "Customer_Loyalty", "Balance", "Service_Level"])
        #df = read_frame(qs)

        df['Age'] = np.where((df['Age']== '60 +'), 0, (np.where((df['Age'] == '36 - 59'), 1, 2)))
        df['Education'] = np.where((df['Education']== 'Highschool and below'), 0,  1)
        df['Employment'] = np.where((df['Employment']== 'Student'), 0, (np.where((df['Employment'] == 'Contract'), 1, 0)))
        df['Employer_Stability'] = np.where((df['Employer_Stability']== 'Unstable'), 0,  1)
        df['Residential_Status'] = np.where((df['Residential_Status'] == 'Rented'), 0,  1)
        df['Salary'] = np.where(((df['Salary'] >= 150) & (df['Salary'] <= 1000)), 0, (np.where(((df['Salary'] > 1000) & (df['Salary'] <= 10000)), 1, 2)))
        df['Customer_Loyalty'] = np.where((df['Customer_Loyalty'] <= 3), 0,  1)
        df['Balance'] = np.where(((df['Balance'] >= 150) & (df['Balance'] <= 2500)), 0, (np.where(((df['Balance'] > 2500) & (df['Balance'] <= 10000)), 1, 2)))

        added = (df['Age'])+(df['Education'])+(df['Employment'])+(df['Salary'])+(df['Employer_Stability'])+(df['Customer_Loyalty'])+(df['Balance'])+(df['Residential_Status'])

        silver = np.where( added <= 11)

        gold = np.where(( added > 11) & (added <= 15))

        platinum = np.where((added > 15) & (added <= 21))


        print (platinum)
        print(silver)
        print(gold)

        if silver:
            customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
            silver_customers.append(customer.Name)
        elif gold:
            customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
            gold_customers.append(customer.Name)
        elif platinum:
            customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
            platinum_customers.append(customer.Name)
        else:
            customer.Service_Level = Service.objects.get(service_name = "No Service Package")
            non_customers.append(customer.name)

        # else:
        #      message = "This customer does not meet the required criteria"
        customer.save()

        if platinum_customers:
            message = 'The following customers are now Platinum Customers: {}'.format(', '.join(platinum_customers))
        if silver_customers:
            message = 'The following customers are now Silver Customers: {}'.format(', '.join(silver_customers))
        if gold_customers:
            message = 'The following customers are now Gold Customers: {}'.format(', '.join(gold_customers))
        if not platinum_customers and not silver_customers and not gold_customers:
            message = 'No customer changes made!'
        ModelAdmin.message_user(request, message, level=SUCCESS)
allocate_service.short_description = 'Allocate Service'






# def allocate_service(ModelAdmin, request, queryset):
#     platinum_customers = []
#     silver_customers = []
#     gold_customers = []
#     non_customers = []
#     message = ''
#
#
#     for customer in queryset:
#         # This class allows function addition, multiplicationn, division etc.
#         class operable:
#             def __init__(self, f):
#                 self.f = f
#             def __call__(self, x):
#                 return self.f(x)
#
#         def op_to_function_op(op):
#             def function_op(self, operand):
#                 def f(x):
#                     return op(self(x), operand(x))
#                 return operable(f)
#             return function_op
#
#         for name, op in [(name, getattr(operator, name)) for name in dir(operator) if "__" in name]:
#             try:
#                 op(1,2)
#             except TypeError:
#                 pass
#             else:
#                 setattr(operable, name, op_to_function_op(op))
#
#
#         @operable
#         def getAge():
#             age = 0
#             #if customer.Age == '60 +':
#             if customer.Age == Customer.objects.get(Age = "60 +"):
#                 age = 0
#             #elif customer.Age == '36 - 59':
#             elif customer.Age == Customer.objects.get(Age = "36 - 59"):
#                 age = 1
#             else:
#                 age = 2
#             print(age)
#             return int(age)
#
#
#         def getEducation():
#             education = 0
#             if customer.Education == Customer.objects.get(Education = "Highschool and below"):
#                 education = 0
#             else:
#                 education = 1
#             return int(education)
#
#         def getEmployment():
#             employment = 0
#             if customer.Employment == Customer.objects.get(Employment = "Student"):
#                 employment = 0
#             elif customer.Employment == Customer.objects.get(Employment = "Contract"):
#                 employment = 1
#             else:
#                 employment = 2
#             return int(employment)
#
#         def getStability():
#             stability = 0
#             if customer.Employer_Stability == Customer.objects.get(Employer_Stability = "Unstable"):
#                 stability = 0
#             else:
#                 stability = 1
#             return int(stability)
#
#         def getResidential():
#             residential = 0
#             if customer.Residential_Status == Customer.objects.get(Residential_Status = "Rented"):
#                 residential = 0
#             else:
#                 residential = 1
#             return int(residential)
#
#         def getSalary():
#             salary = 0
#             if customer.Salary == Customer.objects.get(Salary <= 1000):
#                 salary = 0
#             elif customer.Salary == Customer.objects.get(Salary <= 10001 and Salary > 1000):
#                 salary = 1
#             else:
#                 salary = 2
#             return int(salary)
#
#         def getLoyalty():
#             loyalty = 0
#             loy = Customer.objects.get(Customer_Loyalty <= 2)
#             #if customer.Customer_Loyalty == Customer.objects.get(Customer_Loyalty <= 2):
#             if customer.Customer_Loyalty == loy.Customer_Loyalty:
#                 loyalty = 0
#             else:
#                 loyalty = 1
#             return loyalty
#
#         def getBalance():
#             balance = 0
#             if customer.Balance == Customer.objects.get(Balance <= 2500):
#                 balance = 0
#             elif customer.Balance == Customer.objects.get(Balance <= 10001 and Balance > 2500):
#                 balance = 1
#             else:
#                 balance = 2
#             return int(balance)
#
#
#         def feat_list():
#             total = getAge + getEducation + getEmployment + getStability + getResidential + getSalary + getLoyalty + getBalance
#             return total
#
#         #customer = [(Customer.objects.values("Gender", "Account_Type", "Age","Education", "Employment", "Employer_Stability", "Residential_Status", "Salary", "Customer_Loyalty", "Balance").get(pk=customer.Customer_ID))]
#         flist = feat_list()
#         loyal = getLoyalty
#         #a = getAge()
#         print(flist)
#         print type(flist)
#         print(loyal)
#         print type(loyal)
#         #print(a)
#
#         # if flist > 15 and flist <= 21:
#         #     customer.Service_Level = Service.objects.get(service_name = "Platinum Package")
#         #     platinum_customers.append(customer.Name)
#         # elif flist > 11 and flist <= 15 :
#         #         customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
#         #         gold_customers.append(customer.Name)
#         # elif flist > 0 and flist <= 11:
#         #     customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
#         #     silver_customers.append(customer.Name)
#
#
#         if feat_list() <= 11:
#             customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
#             silver_customers.append(customer.Name)
#         #elif feat_list() > 11 and feat_list() <= 15:
#         elif 11 < feat_list() <= 15:
#             # customer.Service_Level = 'Silver Package'
#             customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
#             gold_customers.append(customer.Name)
#         elif feat_list() > 15:
#             customer.Service_Level = Service.objects.get(service_name = "Platinum Package")
#             platinum_customers.append(customer.Name)
#         else:
#             customer.Service_Level = Service.objects.get(service_name = "No Service Package")
#             non_customers.append(customer.name)
#
#         # else:
#         #      message = "This customer does not meet the required criteria"
#         customer.save()
#
#         if platinum_customers:
#             message = 'The following customers are now Platinum Customers: {}'.format(', '.join(platinum_customers))
#         if silver_customers:
#             message = 'The following customers are now Silver Customers: {}'.format(', '.join(silver_customers))
#         if gold_customers:
#             message = 'The following customers are now Gold Customers: {}'.format(', '.join(gold_customers))
#         if not platinum_customers and not silver_customers and not gold_customers:
#             message = 'No customer changes made!'
#         ModelAdmin.message_user(request, message, level=SUCCESS)
# allocate_service.short_description = 'Allocate Service'


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

@admin.register(models.ServiceManager)
class ServiceManagerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">assignment_ind</i>'
    list_display = ('customer', 'service', 'from_date', 'to_date')
    raw_id_fields = ('customer', )
    list_filter = ('service', )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_box</i>'
    list_display = ('Customer_ID', 'Name', 'Gender', 'Nationality', 'Account_Type', 'Salary', 'Balance', 'Service_Level')
    list_per_page = 900
    list_filter = ('Nationality', 'Gender')
    actions = [export_customers, allocate_service]
