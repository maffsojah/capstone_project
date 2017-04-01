# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, render

from material.frontend.views import ModelViewSet, ListModelView

from . import models, forms


@login_required
def change_manager(request, service_pk):
    service = get_object_or_404(models.Service, pk=service_pk)
    form = forms.ChangeManagerForm(service=service, data=request.POST or None)

    if form.is_valid():
        form.save()

    return render(request, 'employees/change_manager.html', {
        'form': form,
        'service': service,
        'model': models.Service
    })


@login_required
def change_salary(request, employee_pk):
    employee = get_object_or_404(models.Employee, pk=employee_pk)
    form = forms.ChangeSalaryForm(employee=employee, data=request.POST or None)

    if form.is_valid():
        form.save()

    salaries = employee.salary_set.all().order_by('from_date')
    salary_data = {
        'labels': [salary.from_date.strftime('%Y-%m-%d') for salary in salaries],
        'datasets': [
            {'data': [salary.salary for salary in salaries], 'label': 'Salary History'}
        ]
    }

    return render(request, 'employees/change_salary.html', {
        'form': form,
        'employee': employee,
        'salary_history': json.dumps(salary_data),
        'model': models.Employee
    })


@login_required
def change_title(request, employee_pk):
    employee = get_object_or_404(models.Employee, pk=employee_pk)
    form = forms.ChangeTitleForm(employee=employee, data=request.POST or None)

    if form.is_valid():
        form.save()

    return render(request, 'employees/change_title.html', {
        'form': form,
        'employee': employee,
        'model': models.Employee
    })


class ServiceEmployeeListView(ListModelView):
    model = models.Employee
    list_display = ('Customer_ID', 'Name', 'Gender', 'Nationality', 'Account_Type', 'Salary')
    template_name = 'employees/service_cutomers.html'

    def get_queryset(self):
        today = timezone.now().date()
        service = get_object_or_404(models.Service, pk=self.kwargs['service_pk'])
        queryset = super(ServiceEmployeeListView, self).get_queryset()

        return queryset.filter(
            serviceemployee__service=service,
            serviceemployee__from_date__lte=today,
            serviceemployee__to_date__gt=today
        )

    def get_context_data(self, **kwargs):
        service = get_object_or_404(models.Service, pk=self.kwargs['service_pk'])
        return super(ServiceEmployeeListView, self).get_context_data(
            service=service, **kwargs)


class EmployeeViewSet(ModelViewSet):
    model = models.Employee
    list_display = ('Customer_ID', 'Name', 'Gender', 'Nationality', 'Account_Type', 'Salary')

    change_salary_view = [
        r'^(?P<employee_pk>.+)/change_salary/$',
        change_salary,
        '{model_name}_change_salary'
    ]

    change_title_view = [
        r'^(?P<employee_pk>.+)/change_title/$',
        change_title,
        '{model_name}_change_title'
    ]

    def current_salary(self, obj):
        salary = obj.salary_set.current()
        return salary.salary if salary is not None else 0


class ServiceViewSet(ModelViewSet):
    model = models.Service
    list_display = ('service_no', 'service_name', 'service_description', 'manager', 'employees')

    change_manager_view = [
        r'^(?P<service_pk>.+)/change_manager/$',
        change_manager,
        '{model_name}_change_manager'
    ]

    employees_list_view = [
        r'^(?P<service_pk>.+)/employees/$',
        ServiceEmployeeListView.as_view(viewset=EmployeeViewSet()),
        '{model_name}_employees'
    ]

    def manager(self, obj, today=None):
        if today is None:
            today = timezone.now().date()
        manager = obj.servicemanager_set.filter(
            from_date__lte=today,
            to_date__gt=today
        ).first()
        return manager.employee if manager is not None else ''

    def employees(self, obj):
        return obj.serviceemployee_set.count()
