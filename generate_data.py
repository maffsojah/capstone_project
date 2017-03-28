#!/usr/bin/python

import pandas as pd
import numpy as np
import csv
import random

from faker import Faker
from time import time

fake = Faker()

# changing column data with faker

accounts_list = ['Savings', 'Current']
sex_list = ['Male', 'Female']
nationality = ['Zimbabwean', 'Zimbabwean', 'Zimbabwean', 'Zimbabwean', 'Zimbabwean', 'Zimbabwean', 'African', 'African', 'African', 'African', 'European', 'American', 'Asian', 'Asian']
# names_list = [fake.name_female(), fake.name_male()]

# Data Generator function
 
def fake_data():
    return{'Name': fake.name(), 
           'Gender': random.choice(sex_list),
           'Address': fake.street_address(), 
           'Nationality': random.choice(nationality), 
           'Account_Type': random.choice(accounts_list), 
           'Age': random.randint(0, 2), 
           'Education': random.randint(0, 1), 
           'Employment': random.randint(0, 2),
           'Salary': random.randint(0, 2),
           'Employer_Stability': random.randint(0, 1),
           'Customer_Loyalty': random.randint(0, 1),
           'Balance': random.randint(0, 2),
           'Residential_Status': random.randint(0, 1)
          }

t0 = time()

myData = pd.DataFrame([fake_data() for _ in range(1000)], columns = ['Name', 'Gender', 'Address', 'Nationality', 'Account_Type', 'Age','Education', 'Employment', 'Salary', 'Employer_Stability', 'Customer_Loyalty', 'Balance', 'Residential_Status'])
myData.index.names = ['Customer_ID']

tt = time() - t0


print '1 thousand rows of data generated in {} seconds'.format(round(tt, 3))



#myData.to_csv('../datasets/dummyTrain.csv')
 
# Generate classes 'Service_Levels' for the customers using the following criteria,

# Number of features = '8', Total_Weight of features = '12', Number of classes = '3',

# Conditions: 
#    Class 0 (Silver) = weight(0 - 6),
#    Class 1 (Gold) = weight(7 - 8)
#    Class 2 (Platinum) = weight(9 - 12)


myData['Service_Level'] = np.where(((myData['Age'])+(myData['Education'])+(myData['Employment'])+(myData['Salary'])+(myData['Employer_Stability'])+(myData['Customer_Loyalty'])+(myData['Balance'])+(myData['Residential_Status']) <= 6), 0,
                               (np.where((((myData['Age'])+(myData['Education'])+(myData['Employment'])+(myData['Salary'])+(myData['Employer_Stability'])+(myData['Customer_Loyalty'])+(myData['Balance'])+(myData['Residential_Status']) > 6) & ((myData['Age'])+(myData['Education'])+(myData['Employment'])+(myData['Salary'])+(myData['Employer_Stability'])+(myData['Customer_Loyalty'])+(myData['Balance'])+(myData['Residential_Status']) <= 8)), 1, 2)))


# convert the engineered values into real customer details

myData['Service_Level'] = np.where((myData['Service_Level'] == 0), 'Silver', (np.where((myData['Service_Level'] == 1), 'Gold', 'Platinum')))

myData['Employment'] = np.where((myData['Employment']== 0), 'Student', (np.where((myData['Employment'] == 1), 'Contract', 'Permanent')))

myData['Education'] = np.where((myData['Education']== 0), 'Highschool and less',  'Tertiary Education')

myData['Employer_Stability'] = np.where((myData['Employer_Stability']== 0), 'Not Stable',  'Stable')

myData['Residential_Status'] = np.where((myData['Residential_Status'] == 0), 'Rented',  'Owned')
# np.where(('condition1'<= 6), 0, (np.where(('condition2' > 6), 1, 2)))
