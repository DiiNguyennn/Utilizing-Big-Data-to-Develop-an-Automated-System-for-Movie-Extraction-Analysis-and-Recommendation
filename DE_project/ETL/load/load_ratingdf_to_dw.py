# %%
#Import the necessary libraries, create SparkSession with appName as: Insert movie.parquet into DuckDB (movie).
import duckdb
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .appName("Insert rating.parquet into DuckDB (rating)") \
    .getOrCreate()

# %%
parquet_file_path = "/opt/airflow/DE_project/data/parquet/rating.parquet"
#Read Parquet file into PySpark DataFrame
df_rating_spark = spark.read.parquet(parquet_file_path)
#Print out some information of the DataFrame
df_rating_spark.printSchema()
df_rating_spark.show()

# %%
# Convert PySpark DataFrame to Pandas DataFrame
df_rating_pandas = df_rating_spark.toPandas()

# %%
#Path to DuckDB database file
database_path = '/opt/airflow/DE_project/warehouse/datawarehouse.duckdb'
# Connect to DuckDB
conn = duckdb.connect(database=database_path)
conn.execute (''' 
    CREATE TABLE IF NOT EXISTS rating (
        movie_title VARCHAR(255),
        movie_id INT,
        user_id VARCHAR(20),
        author VARCHAR(30),
        rating DECIMAL(10, 2),
        year INT,
        month INT,
        day INT,
        hour INT
);''')

# %%
#Register the Pandas DataFrame as a DuckDB table and insert data into movie
conn.register('df_rating_pandas', df_rating_pandas)
conn.execute('''
    INSERT INTO rating (
        movie_title,
        movie_id,
        user_id,
        author,
        rating,
        year,
        month,
        day,
        hour
    ) SELECT 
        movie_title,
        movie_id,
        user_id,
        author,
        rating,
        year,
        month,
        day,
        hour
    FROM df_rating_pandas
''')
# # Close DuckDB connection
conn.close()
# Stop Spark session
spark.stop()
print("Data has been successfully inserted into table rating in DuckDB!")

# %%
#Check movie table data in datawarehouse
import duckdb
datawarehouse_path = '/opt/airflow/DE_project/warehouse/datawarehouse.duckdb'
conn = duckdb.connect(database=datawarehouse_path)
result = conn.execute("select* from rating limit 10 ").fetchall()
for row in result:
    print(row)
conn.close()

# %% [markdown]
# 


