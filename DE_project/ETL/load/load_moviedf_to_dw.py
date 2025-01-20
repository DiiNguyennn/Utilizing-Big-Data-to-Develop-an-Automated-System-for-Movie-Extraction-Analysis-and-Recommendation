# %%
#Import the necessary libraries, create SparkSession with appName as: Insert movie.parquet into DuckDB (movie).
import duckdb
from pyspark.sql import SparkSession
spark = SparkSession.builder \
    .appName("Insert movie.parquet into DuckDB (movie)") \
    .getOrCreate()

# %%
parquet_file_path = "/opt/airflow/DE_project/data/parquet/movie.parquet"
#Read Parquet file into PySpark DataFrame
df_movie_spark = spark.read.parquet(parquet_file_path)
#Print out some information of the DataFrame
df_movie_spark.printSchema()
df_movie_spark.show()
df_movie_spark.count()

# %%
# Convert PySpark DataFrame to Pandas DataFrame
df_movie_pandas = df_movie_spark.toPandas()

# %%
#Path to DuckDB database file
database_path = '/opt/airflow/DE_project/warehouse/datawarehouse.duckdb'
# Connect to DuckDB
conn = duckdb.connect(database=database_path)
conn.execute (''' 
    CREATE TABLE IF NOT EXISTS movie (
    id INT,
    title VARCHAR(255),
    original_language VARCHAR(10),
    vote_average DECIMAL(3, 1),
    vote_count INT,
    popularity DECIMAL(10, 2),
    runtime INT,
    genre VARCHAR(255),
    release_year INT,
    release_month INT,
    release_day INT
);''')

# %%
#Register the Pandas DataFrame as a DuckDB table and insert data into movie
conn.register('df_movie_pandas', df_movie_pandas)
conn.execute('''
    INSERT INTO movie (
        id,
        title,
        original_language,
        vote_average,
        vote_count,
        popularity,
        runtime,
        genre,
        release_year,
        release_month,
        release_day
    ) SELECT 
        id,
        title,
        original_language,
        vote_average,
        vote_count,
        popularity,
        runtime,
        genre,
        release_year,
        release_month,
        release_day
    FROM df_movie_pandas
''')
# # Close DuckDB connection
conn.close()
# Stop Spark session
spark.stop()
print("Data has been successfully inserted into table movie in DuckDB!")

# %%
#Check movie table data in datawarehouse
import duckdb
datawarehouse_path = '/opt/airflow/DE_project/warehouse/datawarehouse.duckdb'
conn = duckdb.connect(database=datawarehouse_path)
result = conn.execute("select* from movie limit 10 ").fetchall()
for row in result:
    print(row)
conn.close()

