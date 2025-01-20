# %%
#Import the necessary libraries, create SparkSession with appName as: Transform Rating Data.
from pyspark.sql.functions import col, sum, year, month, dayofmonth, hour
from pyspark.sql import SparkSession # type: ignore
spark = SparkSession.builder.appName("Transform Rating Data").getOrCreate()

# %%
#Path to input file.
input_path = '/opt/airflow/DE_project/data/CSV/ratings.csv'
#Read movie data from movei.csv file and output the first 20 lines to the screen.
rating_df = spark.read.format("csv").option("sep",",").option("header","true").option("inferSchema","true").load(input_path)
rating_df.show()

# %%
#Print out the information of the column information.
rating_df.printSchema()

# %%
#Clean data (remove null values ​​and duplicate values).
rating_df_clear = rating_df.dropna()
rating_df_clear = rating_df_clear.dropDuplicates()

# %%
#Check for null values ​​in data and print to screen.
check_null_data = rating_df_clear.select([sum(col(column).isNull().cast("int")).alias(column) for column in rating_df_clear.columns])
check_null_data.show()

# %%
#Check for duplicate values ​​in data and print to screen.
check_duplicate_data = rating_df_clear.groupBy(rating_df_clear.columns).count().filter(col("count")>1)
check_duplicate_data.show()

# %%
#Separate the time column into separate day, month, and year columns for ease of data analysis.
rating_final = rating_df_clear.withColumn("year", year(col("timestamp"))) \
                                .withColumn("month", month(col("timestamp"))) \
                                .withColumn("day", dayofmonth(col("timestamp"))) \
                                .withColumn("hour", hour(col("timestamp")))\
                                .drop("timestamp")
rating_final.show()

# %%
#Path to input file.
output_path = "/opt/airflow/DE_project/data/parquet/rating.parquet"
#Convert data from .csv file to .parquet for convenient storage of large data.
rating_final.write.mode("overwrite").parquet(output_path)
print(f"Data successfully transformed and saved to: {output_path}")

# %%
#Stop spark Session.
spark.stop()