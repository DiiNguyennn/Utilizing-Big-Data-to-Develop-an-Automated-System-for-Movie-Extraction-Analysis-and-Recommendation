# %%
#Import the necessary libraries, create SparkSession with appName as: Transform Movie Data.
from pyspark.sql.functions import col, sum, year, month, dayofmonth, split, explode
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Transform Movie Data").getOrCreate()

# %% [markdown]
# 

# %%
#Path to input file.
input_path = "/opt/airflow/DE_project/data/CSV/movie.csv"
#Read movie data from movei.csv file and output the first 20 lines to the screen.
movie_df = spark.read.format("csv").option("sep",",").option("header","true").option("inferSchema","true").load(input_path)
movie_df.show()

# %%
#Print out the information of the column information.
movie_df.printSchema()

# %%
#Check for null values ​​in data and print output.
check_null_data = movie_df.select([sum(col(column).isNull().cast("int")).alias(column) for column in movie_df.columns])
check_null_data.show()

# %%
#Check for duplicate values ​​in data and print output.
check_duplicate_data = movie_df.groupBy(movie_df.columns).count().filter(col("count") > 1)
check_duplicate_data.show()

# %%
#Clean data (remove null values ​​and duplicate values).
movie_df_cleaned = movie_df.dropna()
movie_df_cleaned = movie_df_cleaned.dropDuplicates()
movie_df_cleaned.show()

# %%
#Check for null values again ​​in the data and print output.
null_data = movie_df_cleaned.select([sum(col(column).isNull().cast("int")).alias(column) for column in movie_df_cleaned.columns])
null_data.show()

# %%
#Check for duplicate values again ​​in the data and print output.
check_duplicate_data = movie_df_cleaned.groupBy(movie_df_cleaned.columns).count().filter(col("count") > 1)
check_duplicate_data.show()

# %%
#Vertical normalization of data and removal of unnecessary columns.
movie_df_cleaned = movie_df_cleaned.withColumn("genre", split(movie_df_cleaned["genres"], ", "))
movie_df_split_genres = movie_df_cleaned.withColumn("genre", explode(movie_df_cleaned["genre"])).drop("genres","overview")
movie_df_split_genres.show()

# %%
#Separate the time column into separate day, month, and year columns for ease of data analysis.
movie_df_final = movie_df_split_genres.withColumn("release_year", year(col("release_date"))) \
                                    .withColumn("release_month", month(col("release_date"))) \
                                    .withColumn("release_day", dayofmonth(col("release_date"))) \
                                    .drop("release_date","adult")
movie_df_final.show() 
movie_df_final.count()

# %%
#Path to input file.
output_path = "/opt/airflow/DE_project/data/parquet/movie.parquet"
#Convert data from .csv file to .parquet for convenient storage of large data.
movie_df_final.write.mode("overwrite").parquet(output_path)
print(f"Data successfully transformed and saved to: {output_path}")

# %%
# Stop Spark session.
spark.stop()


