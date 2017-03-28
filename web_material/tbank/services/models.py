from __future__ import unicode_literals

from django.db import models
from material.frontend import Module

# Create your models here.
class Services(Module):
    Customer_ID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=30)
    Gender = models.CharField(max_length=12)
    Address = models.CharField(max_length=50)
    Nationality = models.CharField(max_length=30)
    Account_Type = models.CharField(max_length=10)
    Age = models.IntegerField(null=False, default=True)
    Education = models.IntegerField(null=False, blank=True, default=0)
    Employment = models.IntegerField(null=False, blank=True, default=0)
    Salary = models.IntegerField(null=False, default=True)
    Employer_Stability = models.IntegerField(null=False, blank=True, default=0)
    Customer_Loyalty = models.IntegerField(null=False, blank=True, default=0)
    Balance = models.IntegerField(null=False, blank=True, default=0)
    Residential_Status = models.IntegerField(null=False, blank=True, default=0)
    Service_Level = models.IntegerField(null=False, blank=True, default=0)

    class Meta:
        db_table = 'services_services'

class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=((None, ''), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')))
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')

    layout = Layout('username', 'email',
                    Row('password', 'password_confirm'),
                    Fieldset('Pesonal details',
                             Row('first_name', 'last_name'),
                             'gender', 'agree_toc'))
