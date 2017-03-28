from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import requests
import csv

from .models import Service, Level

@login_required
# def active_customer_list(request):
#     if not username:
#         username = request.user.username
#
#     # active_customer_list = Service.objects.order_by('-Customer_ID')
#     # context = {'active_customer_list': active_customer_list}
#     parsedData = []
#     data = open('/home/maffsojah/Projects/HIT_400/capstone_project/web_ui/tbank/static/datasets/dummyTrain.csv', 'r')
#     data.next()
#     for line in data:
#         line = line.split(',')
#         customers = Service.objects.filter(user_name=username)
#         context = {'active_customer_list': active_customer_list}
#         customers.Customer_ID = line[0]
#         customers.Name = line[1]
#         customers.Gender = line[2]
#         customers.Address = line[3]
#         customers.Nationality = line[4]
#         customers.Account_Type = line[5]
#         customers.Age = line[6]
#         customers.Education = line[7]
#         customers.Employment = line[8]
#         customers.Salary = line[9]
#         customers.Employer_Stability = line[10]
#         customers.Customer_Loyalty = line[11]
#         customers.Balance = line[12]
#         customers.Residential_Status = line[13]
#         customers.Service_Level = line[14]
#         #customers.save()
#         parsedData.append(customers)
#     #return render(request, 'active_customers.html', {'line': parsedData})
#     #return render(request, 'services/active_customers.html', context, {'line': parsedData})
#         return HttpResponseRedirect(reverse('services:active_customer_list'))
#
#     return render(request, 'services/active_customers.html', context, {'line': parsedData})

def customer_details(request, active_customer_id):
    service = get_object_or_404(Service, pk=active_customer_id)
    return render(request, 'services/active_customers.html', {'service': service})

@login_required
def inactive_customer_list(request):
    if not username:
        username = request.user.username

    # active_customer_list = Service.objects.order_by('-Customer_ID')
    # context = {'active_customer_list': active_customer_list}
    parsedData = []
    data = open('/home/maffsojah/Projects/HIT_400/capstone_project/web_ui/tbank/static/datasets/dummyTest.csv', 'r')
    data.next()
    for line in data:
        line = line.split(',')
        customers = Service.objects.filter(user_name=username)
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
    #return render(request, 'active_customers.html', {'line': parsedData})
    #return render(request, 'services/active_customers.html', context, {'line': parsedData})
        return HttpResponseRedirect(reverse('services:inactive_customer_list'))

    return render(request, 'services/inactive_customers.html', context, {'line': parsedData})

def services_list(request):
    added_services = Level.objects.order_by('-pub_date')[:5]
    context = {'added_services': added_services}
    return render(request, 'services/services_list.html', context)

def service_level_details(request, service_level_id):
    level = get_object_or_404(Level, pk=service_level_id)
    return render(request, 'services/service_level_details.html', {'level':level})


# def active_customers(request):
#     parsedData = []
#     data = open('/home/maffsojah/Projects/HIT_400/capstone_project/web_ui/tbank/static/datasets/dummyTrain.csv', 'r')
#     data.next()
#     for line in data:
#         line = line.split(',')
#         customers = Service.objects.filter()
#         customers.Customer_ID = line[0]
#         customers.Name = line[1]
#         customers.Gender = line[2]
#         customers.Address = line[3]
#         customers.Nationality = line[4]
#         customers.Account_Type = line[5]
#         customers.Age = line[6]
#         customers.Education = line[7]
#         customers.Employment = line[8]
#         customers.Salary = line[9]
#         customers.Employer_Stability = line[10]
#         customers.Customer_Loyalty = line[11]
#         customers.Balance = line[12]
#         customers.Residential_Status = line[13]
#         customers.Service_Level = line[14]
#         #customers.save()
#         parsedData.append(customers)
#     return render(request, 'active_customers.html', {'line': parsedData})
#     #data.close()
#
#
# def inactive_customers(request):
#     parsedData = []
#     data = open('/home/maffsojah/Projects/HIT_400/capstone_project/web_ui/tbank/static/datasets/dummyTest.csv', 'r')
#     data.next()
#     for line in data:
#         line = line.split(',')
#         customers = Services.objects.filter()
#         customers.Customer_ID = line[0]
#         customers.Name = line[1]
#         customers.Gender = line[2]
#         customers.Address = line[3]
#         customers.Nationality = line[4]
#         customers.Account_Type = line[5]
#         customers.Age = line[6]
#         customers.Education = line[7]
#         customers.Employment = line[8]
#         customers.Salary = line[9]
#         customers.Employer_Stability = line[10]
#         customers.Customer_Loyalty = line[11]
#         customers.Balance = line[12]
#         customers.Residential_Status = line[13]
#         #customers.Service_Level = line[14]
#         #customers.save()
#         parsedData.append(customers)
#     return render(request, 'inactive_customers.html', {'line': parsedData})
#     #data.close()
