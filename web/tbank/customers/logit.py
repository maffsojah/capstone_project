#!/usr/bin/python

# Creating Spark SQL temporary views with the DataFrames
## Train View
TrainSet.createOrReplaceTempView("customers")


# SQL can be run over DataFrames that have been registered as a table.
## Train
results = spark.sql("SELECT Gender, Account_Type, Age, Education, Employment, Salary, Employer_Stability, Customer_Loyalty, Balance, Residential_Status, Service_Level FROM customers")
cols = results.columns

categoricalColumns = ["Gender", "Account_Type", "Age","Education", "Employment", "Employer_Stability", "Residential_Status"]
stages = [] # stages in the pipeline

# "Gender","Account_Type",

for categoricalCol in categoricalColumns:

    # Category Indexing with StringIndexer
    stringIndexer = StringIndexer(inputCol=categoricalCol, outputCol=categoricalCol+"Index")

    # Using OneHotEncoder to convert categorical variables into binary SparseVectors
    #encoder = OneHotEncoder(inputCol=categoricalCol+"Index", outputCol=categoricalCol+"classVec")
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
# - fit() computes feature statistics as needed
# - transform() actually transforms the features
pipelineModel = pipeline.fit(results)
results = pipelineModel.transform(results)

# Keep relevant columns
selectedcols = ["label", "features"] + cols
TrainingData = results.select(selectedcols)

(trainData, testData) = TrainingData.randomSplit([0.7, 0.3], seed = 100)

reg = LogisticRegression(labelCol="label", featuresCol="features", maxIter=1000, regParam=0.01, family="multinomial" )
regModel = reg.fit(trainData)

predict = regModel.transform(testData)
predict.select("prediction", "label", "features").show()

evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predict)


h
reg_path = temp_path + '/reg'
reg.save(reg_path)
model2 = LogisticRegression.load(reg_path)
model2.getMaxIter()

model_path = temp_path + 'reg_model'
regModel.save(model_path)
model2 = LogisticRegressionModel.load(model_path)

print("Test Error = %g " % (1.0 - accuracy))
print("Accuracy = %g " % (accuracy * 100))
print("Coefficients: \n" + str(regModel.coefficientMatrix))
print("Intercept: " + str(regModel.interceptVector))
print("coefficientMatrix check = %g " % (regModel.coefficientMatrix[0, 1] == model2.coefficientMatrix[0, 1]))
print("interceptVector check = %g " % (regModel.interceptVector == model2.interceptVector))


if __name__ == "__main__":

    import os
    #del os.environ['PYSPARK_SUBMIT_ARGS']
    import tempfile
    from pyspark.ml.classification import LogisticRegression, LogisticRegressionModel
    from pyspark.ml.evaluation import MulticlassClassificationEvaluator
    from pyspark.ml import Pipeline
    from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
    from pyspark.sql.types import *

    from pyspark.sql import SparkSession

    spark = SparkSession.builder\
        .setMaster('local[*]')\
        .appName('Multiclass Classification: TBank')\
        .getOrCreate()


    TrainSet = spark.read.csv('hdfs://localhost:9000/user/hduser/datasets/oneMill.csv', header='true', inferSchema='true')
    ## save and load model
    temp_path = tempfile.mkdtemp()
    main(spark)
