# Full path and name to your csv file
csv_filepathname='/home/maffsojah/Projects/HIT_400/capstone_project/web/tbank/static/datasets/customers.csv'

# Full path to your django project directory
webproject_home='/home/maffsojah/Projects/HIT_400/capstone_project/web/tbank'

import sys, os
sys.path.append(webproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from .models import Customer

import csv

parsedData = []
data = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
data.next()

for line in data:
    line = line.split(',')
    Customer_ID = Customer_ID()
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
    #customers.Service_Level = line[14]
    customer.save()
    parsedData.append(customers)
