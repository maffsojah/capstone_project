import pandas as import pd
import logging
from django.db import connection
import findspark
findspark.init()
import tempfile
from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.sql.types import *

from pyspark.sql import SparkSession

spark = SparkSession.builder\
    .appName('Multiclass Classification: TBank')\
    .getOrCreate()


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


def to_df(queryset):
    try:
        query, params = queryset.query.sql_with_params()
    except EmptyResultSet:
        # Occurs when Django tries to create an expression for a
        # query which will certainyl be Empty
        # e.g. Customer.objects.filter(Name=[])
        return pd.DataFrame()
    return pd.io.sql.read_sql_query(query, connection, params=params)


def allocate_service(ModelAdmin, request, queryset):
    silver_customers = []
    gold_customers = []
    platinum_customers = []
    message = ''

    for customer in queryset:
        df = to_df(customer)
        # Creating Spark SQL temporary views with the DataFrame
        df.createOrReplaceTempView("cust_temp")
        result = spark.sql("SELECT Gender, Account_Type, Age, Education, Employment, Salary, Employer_Stability, Customer_Loyalty, Balance, Residential_Status, Service_Level FROM cust_temp")
        cols = result.columns
        categoricalColumns = ["Gender", "Account_Type", "Age","Education", "Employment", "Employer_Stability", "Residential_Status"]
        stages = [] # stages in the pipeline

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
        # Transform all features into a vector using VectorAssembler
        numericCols = ["Salary", "Customer_Loyalty", "Balance"]
        assemblerInputs = map(lambda c: c + "classVec", categoricalColumns) + numericCols
        assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
        stages += [assembler]
        # Creating a Pipeline for Training
        pipeline = Pipeline(stages=stages)
        # Running the feature transformations.
        pipelineModel = pipeline.fit(result)
        result = pipelineModel.transform(result)
        # Keep relevant columns
        selectedcols = ["label", "features"] + cols
        predictSet = result.select(selectedcols)
        reg2 = LogisticRegression.load(reg_path)
        regModel2 = LogisticRegressionModel.load(model_path)
        predict = regModel2.transform(predictSet)
        predict.select("prediction", "label", "features").show()

    if predict.select("prediction") == 0.0:
        customer.Service_Level = Service.objects.get(service_name = 'Silver Package')
        silver_customers.append(customer.Name)

    elif predict.select("prediction") == 1.0:
        customer.Service_Level = Service.objects.get(service_name = 'Gold Package')
        gold_customers.append(customer.Name)

    else:
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
