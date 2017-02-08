#!/usr/bin/python
from faker import Faker
from random import random
from sklearn.datasets import make_classification
import pandas as pd
import numpy as np
import csv
import random


fake = Faker()

# changing column data with faker

accounts_list = ['Savings', 'Current']
sex_list = ['Male', 'Female']
# names_list = [fake.name_female(), fake.name_male()]

# Fake Data Generator function
 
def fake_data():
    return{'Name': fake.name(), 
           'Gender': random.choice(sex_list),
           'Address': fake.street_address(), 
           'Nationality': 'Zimbabwean', 
           'Account_Type': random.choice(accounts_list), 
           'Age': random.randint(0, 2), 
           'Education': random.random() > 0.5, 
           'Employment': random.randint(0, 2),
           'Salary': random.randint(0, 2),
           'Employer_Stability': random.random() > 0.5,
           'Consistency': random.random() > 0.5,
           'Balance': random.randint(0, 2),
           'Residential_Status': random.random() > 0.5
          }


df = pd.DataFrame([fake_data() for _ in range(10)], columns = ['Name', 'Gender', 'Address', 'Nationality', 'Account_Type', 'Age','Education', 'Employment', 'Salary', 'Employer_Stability', 'Consistency', 'Balance', 'Residential_Status'])

# define Index for the DataFrame

df.index.names = ['Customer_ID']

#df.head()
#df.dtypes

# print the DataFrame to CSV file
df.to_csv('train_data.csv')

