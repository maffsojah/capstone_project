# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, render

from material.frontend.views import ModelViewSet, ListModelView

from . import models, forms


# @login_required
# def change_manager(request, service_pk):
#     service = get_object_or_404(models.Service, pk=service_pk)
#     form = forms.ChangeManagerForm(service=service, data=request.POST or None)
#
#     if form.is_valid():
#         form.save()
#
#     return render(request, 'customers/change_manager.html', {
#         'form': form,
#         'service': service,
#         'model': models.Service
#     })

@login_required
def change_salary(request, customer_pk):
    customer = get_object_or_404(models.Customer, pk=customer_pk)
    form = forms.ChangeSalaryForm(customer=customer, data=request.POST or None)

    if form.is_valid():
        form.save()

    salaries = customer.salary_set.all().order_by('from_date')
    salary_data = {
        'labels': [salary.from_date.strftime('%Y-%m-%d') for salary in salaries],
        'datasets': [
            {'data': [salary.salary for salary in salaries], 'label': 'Salary History'}
        ]
    }

    return render(request, 'customers/change_salary.html', {
        'form': form,
        'customer': customer,
        'salary_history': json.dumps(salary_data),
        'model': models.Customer
    })

# @login_required
# def change_title(request, customer_pk):
#     customer = get_object_or_404(models.Customer, pk=customer_pk)
#     form = forms.ChangeTitleForm(customer=customer, data=request.POST or None)
#
#     if form.is_valid():
#         form.save()
#
#     return render(request, 'customers/change_title.html', {
#         'form': form,
#         'customer': customer,
#         'model': models.Customer
#     })

class ServiceCustomerListView(ListModelView):
    model = models.Customer
    list_display = ('Customer_ID', 'Name', 'Gender', 'Nationality', 'Account_Type', 'Balance')
    template_name = 'customers/service_cutomers.html'

    def get_queryset(self):
        today = timezone.now().date()
        service = get_object_or_404(models.Service, pk=self.kwargs['service_pk'])
        queryset = super(ServiceCustomerListView, self).get_queryset()

        return queryset.filter(
            servicecustomer__service=service,
            servicecustomer__from_date__lte=today,
            servicecustomer__to_date__gt=today
        )

    def get_context_data(self, **kwargs):
        service = get_object_or_404(models.Service, pk=self.kwargs['service_pk'])
        return super(ServiceCustomerListView, self).get_context_data(
            service=service, **kwargs)

class CustomerViewSet(ModelViewSet):
    model = models.Customer
    list_display = ('Customer_ID', 'Name', 'Gender','Age', 'Nationality', 'Address', 'Account_Type', 'Balance', 'Employer_Stability', 'Customer_Loyalty', 'Residential_Status', 'Service_Level')
    paginate_by = 10

    change_salary_view = [
        r'^(?P<customer_pk>.+)/change_salary/$',
        change_salary,
        '{model_name}_change_salary'
    ]

    # change_title_view = [
    #     r'^(?P<customer_pk>.+)/change_title/$',
    #     change_title,
    #     '{model_name}_change_title'
    # ]

    def current_salary(self, obj):
        salary = obj.salary_set.current()
        return salary.salary if salary is not None else 0

class ServiceViewSet(ModelViewSet):
    model = models.Service
    list_display = ('service_no', 'service_name', 'service_description', 'manager', 'customers')

    # change_manager_view = [
    #     r'^(?P<service_pk>.+)/change_manager/$',
    #     change_manager,
    #     '{model_name}_change_manager'
    # ]

    customers_list_view = [
        r'^(?P<service_pk>.+)/customers/$',
        ServiceCustomerListView.as_view(viewset=CustomerViewSet()),
        '{model_name}_customers'
    ]

    def manager(self, obj, today=None):
        if today is None:
            today = timezone.now().date()
        manager = obj.servicemanager_set.filter(
            from_date__lte=today,
            to_date__gt=today
        ).first()
        return manager.customer if manager is not None else ''

    def customers(self, obj):
        return obj.servicecustomer_set.count()
