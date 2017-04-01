# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
import requests
import csv

from material import Layout, Row, Fieldset
from material.frontend.views import ModelViewSet, ListModelView, DetailModelView

from . import models, forms


# class MyModelViewSet(ModelViewSet):
#    model = models.MyModel

# @login_required
# def change_service(request, customer_pk):
#     customer = get_object_or_404(models.Customer, pk=customer_pk)
#     form = forms.ChangeServiceForm(customer=customer, data=request.POST or None)
#
#     if form.is_valid():
#         form.save()
#
#     services = customer.

class ServiceLevelViewSet(ModelViewSet):
    model = models.ServiceLevel
    list_display = ('service_name', 'description', 'pub_date')


# class CustomerLoyaltyViewSet(ModelViewSet):
#     model = models.CustomerLoyalty
#     list_display = ('customer_loyalty')


class CustomerViewSet(ModelViewSet):
    model = models.Customer
    list_display = (
        'Customer_ID', 'Service_Level', 'Name',
        'Gender', 'Address', 'Nationality',
        'Account_Type', 'Age', 'Education',
        'Employment', 'Salary', 'Employer_Stability',
        'Customer_Loyalty', 'Balance', 'Residential_Status',
    )
    #list_display_links = ('Name', 'Service_Level')
    paginate_by = 10

    layout = Layout(
        Row('Name', 'Age','Gender', 'Account_Type'),
        'Service_Level',
        Row('Nationality', 'Education', 'Employment', 'Salary'),
        'Balance'
    )

    # def change_service = [
    #     r'^(?P<>)'
    # ]





    def get_paginate_by(self, queryset):
        # Paginating by specified value in querystring
        return self.request.GET.get('paginate_by', self.paginate_by)
        """
        <form action="." method="get">
            <select name="paginate_by">
                <option>25</option>
                <option>50</option>
                <option>75</option>
                <option>100</option>
            </select>
        </form>
        """


class ActiveCustomerViewSet(ModelViewSet):
    model = models.Customer

    def active_customers(self, request):
        parsedData = []
        data = open('/home/maffsojah/Projects/HIT_400/capstone_project/web/tbank/static/datasets/dummyTrain.csv', 'r')
        data.next()
        for line in data:
            line = line.split(',')
            customers = Customer.objects.filter(user_name=username)
            context = {'active_customer_list': active_customer_list}
            customers.Customer_ID = line[0]
            customers.Name = line[1]
            customers.Gender = line[2]
            customers.Address = line[3]
            customers.Nationality = line[4]
            customers.Account_Type = line[5]
            customers.Age = line[6]
            customers.Education = line[7]
            customers.Employment = line[8]
            customers.Salary = line[9]
            customers.Employer_Stability = line[10]
            customers.Customer_Loyalty = line[11]
            customers.Balance = line[12]
            customers.Residential_Status = line[13]
            customers.Service_Level = line[14]
            #customers.save()
            parsedData.append(customers)
        return render(request, 'active_customers.html', {'line': parsedData})
        return render(request, '/services/active_customers.html', context, {'line': parsedData})
