from django.shortcuts import render, HttpResponse
import requests
import json
import csv

from services.models import Services

# Create your views here.
def index(request):
    return HttpResponse('Hello Terry!')

def active_users(request):
    parsedData = []
    data = open('/home/maffsojah/Projects/HIT_400/capstone_project/web_ui/tbank/services/static/datasets/dummyTrain.csv', 'r')
    data.next()
    for line in data:
        line = line.split(',')
        users = Services.objects.filter()
        users.Customer_ID = line[0]
        users.Name = line[1]
        users.Gender = line[2]
        users.Address = line[3]
        users.Nationality = line[4]
        users.Account_Type = line[5]
        users.Age = line[6]
        users.Education = line[7]
        users.Employment = line[8]
        users.Salary = line[9]
        users.Employer_Stability = line[10]
        users.Customer_Loyalty = line[11]
        users.Balance = line[12]
        users.Residential_Status = line[13]
        users.Service_Level = line[14]
        #users.save()
        parsedData.append(users)
    return render(request, 'services/customers.html', {'line': parsedData})
    #data.close()
