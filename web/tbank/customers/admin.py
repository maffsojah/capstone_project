from django.contrib import admin
from django.contrib.messages import SUCCESS
import csv
from django.http import HttpResponse
from django.db.models import Case, Value, When
from django.db import connection
import operator
import inspect

import pandas as pd
import numpy as np
from django_pandas.io import read_frame

import findspark
findspark.init()
import tempfile
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml.classification import MultilayerPerceptronClassifier, MultilayerPerceptronClassificationModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.sql.types import *
from pyspark.sql import Row

from pyspark.sql import SparkSession
from os.path import join as pjoin

spark = SparkSession.builder\
    .appName('Multiclass Classification: TBank')\
    .config("spark.sql.warehouse.dir", "/home/maffsojah/Projects/HIT_400/capstone_project/web/tbank/spark-warehouse")\
    .getOrCreate()

temp_path = pjoin("/home/maffsojah/Projects/HIT_400/capstone_project/web/tbank/spark-warehouse")

reg_path = temp_path + '/reg2'
model_path = temp_path + '/reg_model2'
# mlp_path = temp_path + "/mlp"
# mlpmodel_path = temp_path + "/mlp_model"

from . import models
from models import Customer, Service


"""
    PLAN A - using model
"""



def update_service(ModelAdmin, request, queryset):
    silver_customers = []
    gold_customers = []
    platinum_customers = []
    message = ''

    for customer in queryset:
        qs = Customer.objects.all()
        #qs = Customer.objects.latest('Customer_ID')
        df = qs.to_dataframe(fieldnames=["Gender", "Account_Type", "Age", "Education", "Employment", "Employer_Stability", "Residential_Status", "Salary", "Customer_Loyalty", "Balance", "Service_Level"])
        df = spark.createDataFrame(df, schema=None, samplingRatio=None, verifySchema=True)
        # Creating Spark SQL temporary views with the DataFrame
        df.createOrReplaceTempView("cust_temp")
        result = spark.sql("SELECT Gender, Account_Type, Age, Education, Employment, Salary, Employer_Stability, Customer_Loyalty, Balance, Residential_Status, Service_Level FROM cust_temp")
        result.show()
        cols = result.columns
        categoricalColumns = ["Gender", "Account_Type", "Age", "Education", "Employment", "Employer_Stability", "Residential_Status"]
        stages = [] # stages in the pipeline
        #
        for categoricalCol in categoricalColumns:
            # Category Indexing with StringIndexer
            stringIndexer = StringIndexer(inputCol=categoricalCol, outputCol=categoricalCol+"Index")
            # Using OneHotEncoder to convert categorical variables into binary SparseVectors
            encoder = OneHotEncoder(inputCol=stringIndexer.getOutputCol(), outputCol=categoricalCol+"classVec")
            # Adding the stages: will be run all at once later on
            stages += [stringIndexer, encoder]
        # convert label into label indices using the StringIndexer
        label_stringIdx = StringIndexer(inputCol = "Service_Level", outputCol = "label")
        stages += [label_stringIdx]
        # # Transform all features into a vector using VectorAssembler
        numericCols = ["Salary", "Customer_Loyalty", "Balance"]
        assemblerInputs = map(lambda c: c + "classVec", categoricalColumns) + numericCols
        assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
        stages += [assembler]

        # # Creating a Pipeline for Training
        pipeline = Pipeline(stages=stages)
        #Running the feature transformations.
        pipelineModel = pipeline.fit(result)
        result = pipelineModel.transform(result)
        # Keep relevant columns
        selectedcols = ["label", "features"] + cols #"label", "features"
        predictSet = result.select(selectedcols)
        #reg = LogisticRegression(labelCol="label", featuresCol="features", maxIter=1000, regParam=0.01, family="multinomial" )
        reg2 = LogisticRegression.load(reg_path)
        regModel2 = LogisticRegressionModel.load(model_path)
        #predict = regModel2.transform(predictSet)
        predict = regModel2.transform(predictSet).head().prediction

        # ## {Prediction with Perceptron
        # mlp2 = MultilayerPerceptronClassifier.load(mlp_path)
        # mlpmodel2 = MultilayerPerceptronClassificationModel.load(mlpmodel_path)
        #predict = mlpmodel2.transform(predictSet).head().prediction
        #predict.select("prediction", "label", "features").show()
        print(predict)


    #if predict.select("prediction") == 0.0:
    if predict == 0.0:
        customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
        silver_customers.append(customer.Name)

    #elif predict.select("prediction") == 1.0:
    elif predict == 1.0:
        customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
        gold_customers.append(customer.Name)

    else: # predict == 2.0:
        customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
        platinum_customers.append(customer.Name)

    if silver_customers:
        message = 'The following customers now have the Silver Package: {}'.format(', '.join(silver_customers))
    if gold_customers:
        message = 'The following customers now have the Gold Package {}'.format(', '.join(gold_customers))
    if platinum_customers:
        message = 'The following customers now have the Platinum Package {}'.format(', '.join(platinum_customers))
    if not silver_customers and not gold_customers and not platinum_customers:
        message = 'No customer changes have been made!'
    ModelAdmin.message_user(request, message, level=SUCCESS)
update_service.short_description = 'Update Service'
spark.catalog.dropTempView("cust_temp")



"""
    RECOMENDATION FROM PANEL 11/05/2017
    Platinum Package should not always rely on bank balance and salary. It should also consider
    features like Residential_Status, Customer_Loyalty etc.
"""

def allocate_service(ModelAdmin, request, queryset):
    platinum_customers = []
    silver_customers = []
    gold_customers = []
    non_customers = []
    message = ''


    for customer in queryset:
        if   (5000 <= customer.Salary > 10000 and customer.Customer_Loyalty > 4 and customer.Employer_Stability == 'Stable' or
                    customer.Residential_Status == 'Owned' or 500 <= customer.Balance > 10000):
                customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
                platinum_customers.append(customer.Name)


        elif (2500 < customer.Salary <= 6000 and 7 >= customer.Customer_Loyalty > 4 and
                            2500 < customer.Balance <= 10000  and
                                            customer.Education == 'Highschool and below' ) :
                                            #or customer.Education == 'Tertiary and above'
                                            #or customer.Employment == 'Contract'
            customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
            gold_customers.append(customer.Name)

            # if (2500 < customer.Salary <= 6000 and 7 >= customer.Customer_Loyalty > 4 and
            #                     2500 < customer.Balance <= 10000 and
            #                                 customer.Employer_Stability == 'Stable' and customer.Employment == 'Contract'):
            #     customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
            #     gold_customers.append(customer.Name)
            #
            # if (2500 < customer.Salary <= 6000 and 7 >= customer.Customer_Loyalty > 4 and
            #                     2500 < customer.Balance <= 10000 and
            #                                 customer.Employer_Stability == 'Stable' and customer.Education == 'Tertiary and above' or customer.Employment == 'Contract'):
            #     customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
            #     gold_customers.append(customer.Name)
            #
            # if (customer.Customer_Loyalty >= 7 and customer.Employer_Stability == 'Stable' and 2500 < customer.Salary <= 6000 ):
            #      customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
            #      gold_customers.append(customer.Name)

        elif (customer.Salary <= 100  and customer.Employer_Stability == 'Unstable' and
                customer.Customer_Loyalty < 4 and customer.Balance <= 300 or customer.Residential_Status == 'Rented' ):
                # or customer.Employment == 'Contract'
            customer.Service_Level = Service.objects.get(service_name = "No Service Package")
            non_customers.append(customer.Name)

        else:
            customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
            silver_customers.append(customer.Name)

        # if (1 <= customer.Customer_Loyalty <= 3 and customer.Salary  ):
        #     customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
        #     silver_customers.append(customer.Name)
        customer.save()

        if platinum_customers:
            message = 'The following customers are now Platinum Customers: {}'.format(', '.join(platinum_customers))
        if silver_customers:
            message = 'The following customers are now Silver Customers: {}'.format(', '.join(silver_customers))
        if gold_customers:
            message = 'The following customers are now Gold Customers: {}'.format(', '.join(gold_customers))
        if non_customers:
            message = 'The following customers have no Service Packages: {}'.format(', '.join(non_customers))
        if not platinum_customers and not silver_customers and not gold_customers and not non_customers:
            message = 'No customer changes made!'
        ModelAdmin.message_user(request, message, level=SUCCESS)
allocate_service.short_description = 'Allocate Service'


def export_customers(ModelAdmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Customer_ID', 'Name', 'Gender','Age', 'Nationality', 'Education', 'Address', 'Account_Type', 'Employment', 'Salary', 'Balance', 'Employer_Stability', 'Customer_Loyalty', 'Residential_Status', 'Service_Level'])
    customers = queryset.values_list('Customer_ID', 'Name', 'Gender','Age', 'Nationality', 'Education', 'Address', 'Account_Type', 'Employment', 'Salary', 'Balance', 'Employer_Stability', 'Customer_Loyalty', 'Residential_Status', 'Service_Level')
    for customer in customers:
        writer.writerow(customer)
    return response
    export_customers.short_description = 'Export to csv'

@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_balance</i>'
    list_display = ( 'service_name', 'service_description') # 'service_no',

@admin.register(models.ServiceCustomer)
class ServiceCustomerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">people_outline</i>'
    list_display = ('customer', 'service', 'from_date', 'to_date')
    list_select_related = True
    raw_id_fields = ('customer', )
    list_filter = ('service', )
    list_per_page = 10
    # inlines = [
    #     CustomerInline,
    # ]

@admin.register(models.ServiceManager)
class ServiceManagerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">assignment_ind</i>'
    list_display = ('customer', 'service', 'from_date', 'to_date')
    raw_id_fields = ('customer', )
    list_filter = ('service', )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">account_box</i>'
    list_display = ('Customer_ID', 'Name', 'Gender', 'Nationality', 'Account_Type', 'Salary', 'Balance', 'Service_Level')
    list_per_page = 900
    list_filter = ('Nationality', 'Gender')
    actions = [export_customers, allocate_service, update_service]
