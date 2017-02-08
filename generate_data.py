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


df = pd.DataFrame([fake_data() for _ in range(100000)], columns = ['Name', 'Gender', 'Address', 'Nationality', 'Account_Type', 'Age','Education', 'Employment', 'Salary', 'Employer_Stability', 'Consistency', 'Balance', 'Residential_Status'])

# define Index for the DataFrame

df.index.names = ['Customer_ID']

# Creates ['Service_Level'] column with either 0 for Silver, 1 for Gold or 2 for Platinum Level 

df['Service_Level'] = np.where((df['Age']==1)&(df['Education']==True)&(df['Employment']==2)&(df['Salary']==0)&(df['Employer_Stability']==False)&(df['Consistency']==True)&(df['Balance']==0)&(df['Residential_Status']==False), 0,
                               (np.where((df['Age']==1)&(df['Education']==True)&(df['Employment']==2)&(df['Salary']==2)&(df['Employer_Stability']==False)&(df['Consistency']==True)&(df['Balance']==2)&(df['Residential_Status']==True), 2, 1)))


# print the DataFrame to CSV file

df.to_csv('train_data.csv')

