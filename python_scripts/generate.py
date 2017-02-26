import pandas as pd
import numpy as np
import csv
import random

from faker import Faker


fake = Faker()


# Accounts and Gender lists

accounts_list = ['Savings', 'Current']

sex_list = ['Male', 'Female']


# generate fake data

def fake_data():
    return {'Name': fake.name(),
            'Gender': random.choice(sex_list),
            'Address': fake.street_address(),
            'Nationality': 'Zimbabwean',
            'Account_Type': random.choice(accounts_list),
            'Age': random.randint(0,2) ,
            'Salary': random.randint(0, 2),
            'Employer_Stability': random.randint(0, 1),
            'Customer_Loyalty': random.randint(0, 1),
            'Education_Level': random.randint(0, 1), 
            'Employment_Status': random.randint(0, 2),
            'Balance': random.randint(0, 2),
            'Residential_Status': random.randint(0, 1)

myData = pd.DataFrame([fake_data() for _ in range(1000)], columns=['Name', 'Gender', 'Address',
                                                                   'Nationality', 'Account_Type',
                                                                   'Age', 'Salary',
                                                                   'Employer_Stability',
                                                                   'Customer_Loyalty',
                                                                   'Education_Level',
                                                                   'Employment_Status', 'Balance',
                                                                   'Residential_Status'])
myData.index.names = ['Customer_ID']


#myData['Service_Level'] = np.where()




myData.to_csv('../datasets/trainDataOne.csv')


