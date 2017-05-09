from django.contrib import admin
from django.contrib.messages import SUCCESS
import csv
from django.http import HttpResponse
from django.db.models import Case, Value, When
from django.db import connection
import operator
#from django.db.models.sql.datastructures import EmptyResultSet

import pandas as pd
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

spark = SparkSession.builder\
    .appName('Multiclass Classification: TBank')\
    .getOrCreate()

from . import models
from models import Customer, Service


## Custom Action for the customers
# def to_df(queryset):
#     try:
#         query, params = queryset.query.sql_with_params()
#     except EmptyResultSet:
#         # Occurs when Django tries to create an expression for a
#         # query which will certainyl be Empty
#         # e.g. Customer.objects.filter(Name=[])
#         return pd.DataFrame()
#     return pd.io.sql.read_sql_query(query, connection, params=params)

#####  PLAN B ALLOCATION

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

@operable
def age(ModelAdmin, request, queryset):
    age = 0
    if customer.Age == '60 +':
        age = 0
    elif customer.Age == '36 - 59':
        age = 1
    else:
        age = 2
    return age

def education(ModelAdmin, request, queryset):
    education = 0
    if customer.Education == 'Highschool and below':
        education = 0
    else:
        education = 1
    return education

def employment(ModelAdmin, request, queryset):
    employment = 0
    if customer.Employment == 'Student':
        employment = 0
    elif customer.Employment == 'Contract':
        employment = 1
    else:
        employment = 2
    return employment

def stability(ModelAdmin, request, queryset):
    stability = 0
    if customer.Employer_Stability == 'Unstable':
        stability = 0
    else:
        stability = 1
    return stability

def residential(ModelAdmin, request, queryset):
    residential = 0
    if customer.Residential_Status == 'Rented':
        residential = 0
    else:
        residential = 1
    return residential

def salary(ModelAdmin, request, queryset):
    salary = 0
    if customer.Salary <= 1000:
        salary = 0
    elif 1000 < customer.Salary <= 10001:
        salary = 1
    else:
        salary = 2
    return salary

def loyalty(ModelAdmin, request, queryset):
    loyalty = 0
    if customer.Customer_Loyalty <= 2:
        loyalty = 0
    else:
        loyalty = 1
    return loyalty

def balance(ModelAdmin, request, queryset):
    balance = 0
    if customer.Balance <= 2500:
        balance = 0
    elif 2500 < customer.Balance <= 10001:
        balance = 1
    else:
        balance = 2
    return balance

#def feat_list(age, education, employment, stability, residential, salary, loyalty, balance):
def feat_list():
    total = age + education + employment + stability + residential + salary + loyalty + balance
    return total

# def main():
#     age = age()
#     education = education()
#     employment = employment()
#     stability = stability()
#     residential = residential()
#     salary = salary()
#     loyalty = loyalty()
#     balance = balance()
# main()

#feat_list = age + education + employment + stability + residential + salary + loyalty + balance

def allocate_service(ModelAdmin, request, queryset):
    platinum_customers = []
    silver_customers = []
    gold_customers = []
    message = ''

    for customer in queryset:
        #Customer.objects.exclude(Customer_ID=Customer_ID)
        if feat_list() <= 11:
            customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
            silver_customers.append(customer.Name)
        elif feat_list() > 11 and feat_list() <= 15:
            # customer.Service_Level = 'Silver Package'
            customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
            gold_customers.append(customer.Name)
        else:
             customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
             platinum_customers.append(customer.Name)
        customer.save()

        if platinum_customers:
            message = 'The following customers are now Platinum Customers: {}'.format(', '.join(platinum_customers))
        if silver_customers:
            message = 'The following customers are now Silver Customers: {}'.format(', '.join(silver_customers))
        if gold_customers:
            message = 'The following customers are now Gold Customers: {}'.format(', '.join(gold_customers))
        if not platinum_customers and not silver_customers and not gold_customers:
            message = 'No customer changes made!'
        ModelAdmin.message_user(request, message, level=SUCCESS)
allocate_service.short_description = 'Allocate Service'


def remove_service(ModelAdmin, request, queryset):
    platinum_customers = []
    silver_customers = []
    gold_customers = []
    message = ''

    for customer in queryset:
        if customer.Service_Level == 'Silver Package':
            #customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
            customer.Service_Level = Customer.objects.get(Service_Level = 'Silver Package')
            customer.Service_Level.delete()
            silver_customers.append(customer.Name)
        elif customer.Service_Level == 'Gold Package':
            # customer.Service_Level = 'Silver Package'
            #customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
            customer.Service_Level = Customer.objects.get(Service_Level = 'Gold Package')
            customer.Service_Level.delete()
            gold_customers.append(customer.Name)
        elif customer.Service_Level == "Platinum Package":
             customer.Service_Level = Customer.objects.get(Service_Level = 'Platinum Package')
             customer.Service_Level.delete()
             platinum_customers.append(customer.Name)
        #customer.save()

        if platinum_customers:
            message = 'The following customers no longer have services: {}'.format(', '.join(platinum_customers))
        elif silver_customers:
            message = 'The following customers no longer have services: {}'.format(', '.join(silver_customers))
        elif gold_customers:
            message = 'The following customers no longer have services: {}'.format(', '.join(gold_customers))
        #if not platinum_customers and not silver_customers and not gold_customers:
        else:
            message = 'No customer changes made!'
        customer.save()
        ModelAdmin.message_user(request, message, level=SUCCESS)
remove_service.short_description = 'Remove Service'

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




# def allocate_service(ModelAdmin, request, queryset):
#     silver_customers = []
#     gold_customers = []
#     platinum_customers = []
#     message = ''
#
#     for customer in queryset:
#         #df = to_df(customer)
#         #df = pd.DataFrame.from_records(customer.objects.all()
#         data = [(customer)]
#
#         # header = data.first()
#         # data.filter(lambda line: line != header)
#         #data = data.zipWithIndex().filter(lambda (row, index): index > 0).keys()
#
#         # def remove_header(itr_index, itr):
#         #     return iter(list(itr)[1:]) if itr_index == 0 else itr
#         # data.mapPartitionsWithIndex(remove_header)
#         #df = spark.createDataFrame(Customer.objects.all())
#         #df = spark.createDataFrame(data.collect()
#         df = spark.createDataFrame(data, schema=None, samplingRatio=None, verifySchema=True)
#         #df.head(10)
#         #df = spark.createDataFrame(data, ['Customer_ID', 'Name', 'Gender','Age', 'Nationality', 'Address', 'Account_Type', 'Salary', 'Balance', 'Employer_Stability', 'Customer_Loyalty', 'Residential_Status', 'Service_Level']).collect()
#         # Creating Spark SQL temporary views with the DataFrame
#         df.createOrReplaceTempView("cust_temp")
#         result = spark.sql("SELECT Gender, Account_Type, Age, Education, Employment, Salary, Employer_Stability, Customer_Loyalty, Balance, Residential_Status, Service_Level FROM cust_temp")
#         result.show()
#         cols = result.columns
#         categoricalColumns = ["Gender", "Account_Type", "Age","Education", "Employment", "Employer_Stability", "Residential_Status"]
#         stages = [] # stages in the pipeline
#
#         for categoricalCol in categoricalColumns:
#             # Category Indexing with StringIndexer
#             stringIndexer = StringIndexer(inputCol=categoricalCol, outputCol=categoricalCol+"Index")
#             # Using OneHotEncoder to convert categorical variables into binary SparseVectors
#             encoder = OneHotEncoder(inputCol=stringIndexer.getOutputCol(), outputCol=categoricalCol+"classVec")
#             # Adding the stages: will be run all at once later on
#             stages += [stringIndexer, encoder]
#         # convert label into label indices using the StringIndexer
#         label_stringIdx = StringIndexer(inputCol = "Service_Level", outputCol = "label")
#         stages += [label_stringIdx]
#         # Transform all features into a vector using VectorAssembler
#         numericCols = ["Salary", "Customer_Loyalty", "Balance"]
#         assemblerInputs = map(lambda c: c + "classVec", categoricalColumns) + numericCols
#         assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
#         stages += [assembler]
#         # Creating a Pipeline for Training
#         pipeline = Pipeline(stages=stages)
#         # Running the feature transformations.
#         pipelineModel = pipeline.fit(result)
#         result = pipelineModel.transform(result)
#         # Keep relevant columns
#         selectedcols = ["label", "features"] + cols
#         predictSet = result.select(selectedcols)
#         reg2 = LogisticRegression.load(reg_path)
#         regModel2 = LogisticRegressionModel.load(model_path)
#         predict = regModel2.transform(predictSet)
#         predict.select("prediction", "label", "features").show()
#
#     if predict.select("prediction") == 0.0:
#         customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
#         silver_customers.append(customer.Name)
#
#     elif predict.select("prediction") == 1.0:
#         customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
#         gold_customers.append(customer.Name)
#
#     else:
#         customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
#         platinum_customers.append(customer.Name)
#
#     if silver_customers:
#         message = 'The following customers now have the Silver Package: {}'.format(', '.join(silver_customers))
#     if gold_customers:
#         message = 'The following customers now have the Gold Package {}'.format(', '.join(gold_customers))
#     if platinum_customers:
#         message = 'The following customers now have the Platinum Package {}'.format(', '.join(platinum_customers))
#     if not silver_customers and not gold_customers and not platinum_customers:
#         message = 'No customer changes have been made!'
#     ModelAdmin.message_user(request, message, level=SUCCESS)
# allocate_service.short_description = 'Allocate Service'
# spark.catalog.dropTempView("cust_temp")

# def allocate_service(ModelAdmin, request, queryset):
#     platinum_customers = []
#     silver_customers = []
#     message = ''
#
#     for customer in queryset:
#         if customer.Salary >= 10000 and customer.Residential_Status == 'Owned' and customer.Employer_Stability == 'Stable':
#             # customer.Service_Level = 'Platinum Package'
#             customer.Service_Level = Service.objects.get(service_name = 'Platinum Package')
#             platinum_customers.append(customer.Name)
#         elif customer.Salary <= 1000 and customer.Residential_Status == 'Rented' and customer.Employer_Stability == 'Unstable':
#             # customer.Service_Level = 'Silver Package'
#             customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
#             silver_customers.append(customer.Name)
#         customer.save()
#
#         if platinum_customers:
#             message = 'The following customers are now platinum: {}'.format(', '.join(platinum_customers))
#         if silver_customers:
#             message = 'The following customers are now silver: {}'.format(', '.join(silver_customers))
#         if not platinum_customers and not silver_customers:
#             message = 'No customer changes!'
#         ModelAdmin.message_user(request, message, level=SUCCESS)
# allocate_service.short_description = 'Allocate Service'



# class CustomerInline(admin.TabularInline):
#     model = Customer


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
    actions = [export_customers, allocate_service, remove_service]


# @admin.register(models.Salary)
# class SalaryAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">account_balance_wallet</i>'
#     list_display = ('customer', 'from_date', 'to_date', 'salary')
#     raw_id_fields = ('customer', )

# @admin.register(models.Title)
# class TitleAdmin(admin.ModelAdmin):
#     icon = '<i class="material-icons">reorder</i>'
#     list_display = ('customer', 'from_date', 'to_date', 'title')
#     raw_id_fields = ('customer', )
#     list_filter = ('title', )
