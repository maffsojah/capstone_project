#!/usr/bin/python


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClassificationEngine:
    """ A customer classification engine
    """

    def __train_model(self):
        """ Train the Multinomial Logistic Regression Model with the current dataset
        """
        logger.info("Training the Multinomial Logit Model...")
        reg = LogisticRegression(labelCol="label", featuresCol="features", maxIter=1000, regParam=0.01, family="multinomial" )
        self.regModel = reg.fit(self.trainData)
        model_path = temp_path + 'reg_model'
        regModel.save(model_path)
        logger.info("Multinomial Logit Model built!")

    def __predict_level(self, cust_data):
        # Load the saved model
        allocateModel = LogisticRegressionModel.load(model_path)

        predict = self.regModel.transform(allocatedData)

        return predict.select("prediction")

    def add_new_data(self, ):
        """ Add data from django model for prediction
        """

    def __init__(self, sc, dataset_path):
        """ Initialise the Classification engine given a spark context/Session and a dataset path
        """

        logger.info("Starting up the Classification Engine")

        self.sc = sc

        # Load the Training and Testing Data for later use
        logger.info("Loading the Prediction Data")
        TrainSet.createOrReplaceTempView("allocate")
        results = spark.sql("SELECT Gender, Account_Type, Age, Education, Employment, Salary, Employer_Stability, Customer_Loyalty,     Balance, Residential_Status, Service_Level FROM allocate")
        cols = results.columns
        categoricalColumns = ["Gender", "Account_Type", "Age","Education", "Employment", "Employer_Stability", "Residential_Status"]
        stages = []

        for categoricalCol in categoricalColumns:
            stringIndexer = StringIndexer(inputCol=categoricalCol, outputCol=categoricalCol+"Index")
            encoder = OneHotEncoder(inputCol=stringIndexer.getOutputCol(), outputCol=categoricalCol+"classVec")
            stages += [stringIndexer, encoder]

        label_stringIdx = StringIndexer(inputCol = "Service_Level", outputCol = "label")
        stages += [label_stringIdx]

        numericCols = ["Salary", "Customer_Loyalty", "Balance"]
        assemblerInputs = map(lambda c: c + "classVec", categoricalColumns) + numericCols
        assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
        stages += [assembler]

        pipeline = Pipeline(stages=stages)
        pipelineModel = pipeline.fit(results)
        results = pipelineModel.transform(results)
        selectedcols = ["label", "features"] + cols
        allocateData = results.select(selectedcols)



        # Train the model
        self.maxIter = 1000
        self.numFolds = 3
        self.reg = 100.0
        self.__train_model()


if __name__ == "__main__":

    import os
    from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
    from pyspark.ml.evaluation import MulticlassClassificationEvaluator
    from pyspark.ml import Pipeline
    from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
    from pyspark.sql.types import *

    from pyspark.sql import SparkSession


    spark = SparkSession.builder\
        .appName('Multiclass Classification: TBank')\
        .getOrCreate()

    sc = spark.sparkContext

    TrainSet = spark.read.csv('hdfs://localhost:9000/user/hduser/datasets/oneMill.csv', header='true', inferSchema='true')
    import tempfile
