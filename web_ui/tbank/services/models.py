from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Level(models.Model):
    SERVICE_LEVELS_CHOICES = (
        (0, 'Silver'),
        (1, 'Gold'),
        (2, 'Platinum')
    )
    service_rating = models.IntegerField(choices=SERVICE_LEVELS_CHOICES)
    comment = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date added')

class Service(models.Model):
    Customer_ID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=30)
    Gender = models.CharField(max_length=12)
    Address = models.CharField(max_length=50)
    Nationality = models.CharField(max_length=30)
    Account_Type = models.CharField(max_length=10)
    Age = models.IntegerField(null=False, default=True)
    Education = models.CharField(max_length=30)
    Employment = models.CharField(max_length=30)
    Salary = models.IntegerField(null=False, default=True)
    Employer_Stability = models.CharField(max_length=30)
    Customer_Loyalty = models.IntegerField(null=False, blank=True, default=0)
    Balance = models.IntegerField(null=False, blank=True, default=0)
    Residential_Status = models.CharField(max_length=30)
    Service_Level = models.ForeignKey(Level)

    class Meta:
        db_table = 'services_services'
