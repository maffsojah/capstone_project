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
#globs['temp_path'] = temp_path
reg_path = temp_path + '/reg2'
model_path = temp_path + '/reg_model2'

from . import models
from models import Customer, Service

#####  PLAN B ALLOCATION


# def allocate_service(ModelAdmin, request, queryset):
#     platinum_customers = []
#     silver_customers = []
#     gold_customers = []
#     non_customers = []
#     message = ''
#
#
#
#     for customer in queryset:
#         qs = Customer.objects.all()
#         df = qs.to_dataframe(fieldnames=["Age","Education", "Employment", "Employer_Stability", "Residential_Status", "Salary", "Customer_Loyalty", "Balance", "Service_Level"])
#         #df = read_frame(qs)
#
#         df['Age'] = np.where((df['Age']== '60 +'), 0, (np.where((df['Age'] == '36 - 59'), 1, 2)))
#         df['Education'] = np.where((df['Education']== 'Highschool and below'), 0,  1)
#         df['Employment'] = np.where((df['Employment']== 'Student'), 0, (np.where((df['Employment'] == 'Contract'), 1, 0)))
#         df['Employer_Stability'] = np.where((df['Employer_Stability']== 'Unstable'), 0,  1)
#         df['Residential_Status'] = np.where((df['Residential_Status'] == 'Rented'), 0,  1)
#         df['Salary'] = np.where(((df['Salary'] >= 150) & (df['Salary'] <= 1000)), 0, (np.where(((df['Salary'] > 1000) & (df['Salary'] <= 10000)), 1, 2)))
#         df['Customer_Loyalty'] = np.where((df['Customer_Loyalty'] <= 3), 0,  1)
#         df['Balance'] = np.where(((df['Balance'] >= 150) & (df['Balance'] <= 2500)), 0, (np.where(((df['Balance'] > 2500) & (df['Balance'] <= 10000)), 1, 2)))
#
#         added = (df['Age'])+(df['Education'])+(df['Employment'])+(df['Salary'])+(df['Employer_Stability'])+(df['Customer_Loyalty'])+(df['Balance'])+(df['Residential_Status'])
#
#         silver = np.where( added <= 11)
#
#         gold = np.where(( added > 11) & (added <= 15))
#
#         platinum = np.where((added > 15) & (added <= 21))
#
#
#         print (platinum)
#         print(silver)
#         print(gold)
#
#         if silver:
#             customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
#             silver_customers.append(customer.Name)
#         elif gold:
#             customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
#             gold_customers.append(customer.Name)
#         elif platinum:
#             customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
#             platinum_customers.append(customer.Name)
#         else:
#             customer.Service_Level = Service.objects.get(service_name = "No Service Package")
#             non_customers.append(customer.name)
#
#         # else:
#         #      message = "This customer does not meet the required criteria"
#         customer.save()
#
#         if platinum_customers:
#             message = 'The following customers are now Platinum Customers: {}'.format(', '.join(platinum_customers))
#         if silver_customers:
#             message = 'The following customers are now Silver Customers: {}'.format(', '.join(silver_customers))
#         if gold_customers:
#             message = 'The following customers are now Gold Customers: {}'.format(', '.join(gold_customers))
#         if not platinum_customers and not silver_customers and not gold_customers:
#             message = 'No customer changes made!'
#         ModelAdmin.message_user(request, message, level=SUCCESS)
# allocate_service.short_description = 'Allocate Service'


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
update_service.short_description = 'Update'
spark.catalog.dropTempView("cust_temp")

# This class allows function addition, multiplicationn, division etc.
class operable:
    def __init__(self, f):
        self.f = f
    def __call__(self, x):
        return self.f(x)

def op_to_function_op(op):
    def function_op(self, operand):
        def f(x):
            return op(self(x), operand(x))
        return operable(f)
    return function_op

for name, op in [(name, getattr(operator, name)) for name in dir(operator) if "__" in name]:
    try:
        op(1,2)
    except TypeError:
        pass
    else:
        setattr(operable, name, op_to_function_op(op))

def allocate_service(ModelAdmin, request, queryset):
    platinum_customers = []
    silver_customers = []
    gold_customers = []
    non_customers = []
    message = ''


    for customer in queryset:

        # @operable
        # def getAge():
        #     age = 0
        #     #if customer.Age == '60 +':
        #     if customer.Age == Customer.objects.get(Age = "60 +"):
        #         age = 0
        #     #elif customer.Age == '36 - 59':
        #     elif customer.Age == Customer.objects.get(Age = "36 - 59"):
        #         age = 1
        #     else:
        #         age = 2
        #     return age
        #
        # @operable
        # def getEducation():
        #     education = 0
        #     if customer.Education == Customer.objects.get(Education = "Highschool and below"):
        #         education = 0
        #     else:
        #         education = 1
        #     return education
        #
        # @operable
        # def getEmployment():
        #     employment = 0
        #     if customer.Employment == Customer.objects.get(Employment = "Student"):
        #         employment = 0
        #     elif customer.Employment == Customer.objects.get(Employment = "Contract"):
        #         employment = 1
        #     else:
        #         employment = 2
        #     return employment
        #
        # @operable
        # def getStability():
        #     stability = 0
        #     if customer.Employer_Stability == Customer.objects.get(Employer_Stability = "Unstable"):
        #         stability = 0
        #     else:
        #         stability = 1
        #     return stability
        #
        # @operable
        # def getResidential():
        #     residential = 0
        #     if customer.Residential_Status == Customer.objects.get(Residential_Status = "Rented"):
        #         residential = 0
        #     else:
        #         residential = 1
        #     return residential
        #
        # @operable
        # def getSalary():
        #     salary = 0
        #     if customer.Salary == Customer.objects.get(Salary <= 1000):
        #         salary = 0
        #     elif customer.Salary == Customer.objects.get(Salary <= 10001 and Salary > 1000):
        #         salary = 1
        #     else:
        #         salary = 2
        #     return salary
        #
        # @operable
        # def getLoyalty():
        #     loyalty = 0
        #     loy = Customer.objects.get(Customer_Loyalty <= 2)
        #     #if customer.Customer_Loyalty == Customer.objects.get(Customer_Loyalty <= 2):
        #     if customer.Customer_Loyalty == loy.Customer_Loyalty:
        #         loyalty = 0
        #     else:
        #         loyalty = 1
        #     return loyalty
        #
        # @operable
        # def getBalance():
        #     balance = 0
        #     if customer.Balance == Customer.objects.get(Balance <= 2500):
        #         balance = 0
        #     elif customer.Balance == Customer.objects.get(Balance <= 10001 and Balance > 2500):
        #         balance = 1
        #     else:
        #         balance = 2
        #     return balance
        #
        #
        # def feat_list():
        #     total = getAge + getEducation + getEmployment + getStability + getResidential + getSalary + getLoyalty + getBalance
        #     #print('total:'+ total)
        #     return total

        #customer = [(Customer.objects.values("Gender", "Account_Type", "Age","Education", "Employment", "Employer_Stability", "Residential_Status", "Salary", "Customer_Loyalty", "Balance").get(pk=customer.Customer_ID))]
        #flist = feat_list()
        # loyal = getLoyalty
        # #a = getAge()
        # print(flist)
        # print type(flist)
        # print(loyal)
        # print type(loyal)
        #print(a)

        # if flist > 15 and flist <= 21:
        #     customer.Service_Level = Service.objects.get(service_name = "Platinum Package")
        #     platinum_customers.append(customer.Name)
        # elif flist > 11 and flist <= 15 :
        #         customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
        #         gold_customers.append(customer.Name)
        # elif flist > 0 and flist <= 11:
        #     customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
        #     silver_customers.append(customer.Name)


        # if feat_list() <= 11:
        #     customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
        #     silver_customers.append(customer.Name)
        # #elif feat_list() > 11 and feat_list() <= 15:
        # elif 11 < feat_list() <= 15:
        #     # customer.Service_Level = 'Silver Package'
        #     customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
        #     gold_customers.append(customer.Name)
        # elif feat_list() > 15:
        #     customer.Service_Level = Service.objects.get(service_name = "Platinum Package")
        #     platinum_customers.append(customer.Name)
        # else:
        #     customer.Service_Level = Service.objects.get(service_name = "No Service Package")
        #     non_customers.append(customer.name)


        if   (customer.Salary > 10000 and customer.Customer_Loyalty > 4 and customer.Employer_Stability == 'Stable' and
                    customer.Residential_Status == 'Owned' or customer.Balance > 10000):
                customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
                platinum_customers.append(customer.Name)

        elif (2500 < customer.Salary <= 10000 and customer.Customer_Loyalty < 4 and
                            2500 < customer.Balance <= 10000 or customer.Employment == 'Contract' and
                                        customer.Employer_Stability == 'Stable'):
            customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
            gold_customers.append(customer.Name)

        elif (customer.Salary <= 100 and customer.Residential_Status == 'Rented' and customer.Employer_Stability == 'Unstable' and
                customer.Customer_Loyalty < 4 or customer.Balance <= 300):
            customer.Service_Level = Service.objects.get(service_name = "No Service Package")
            non_customers.append(customer.Name)

        else:
            customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
            silver_customers.append(customer.Name)
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
    writer.writerow(['Customer_ID', 'Name', 'Gender','Age', 'Nationality', 'Address', 'Account_Type', 'Salary', 'Balance', 'Employer_Stability', 'Customer_Loyalty', 'Residential_Status', 'Service_Level'])
    customers = queryset.values_list('Customer_ID', 'Name', 'Gender','Age', 'Nationality', 'Address', 'Account_Type', 'Salary', 'Balance', 'Employer_Stability', 'Customer_Loyalty', 'Residential_Status', 'Service_Level')
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
