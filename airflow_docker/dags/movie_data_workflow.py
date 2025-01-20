from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Khởi tạo DAG
default_args = {
    'owner': 'diinguyen',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
}

# Tạo DAG
with DAG(
    'movie_data_etl_workflow',
    default_args=default_args,
    description='Workflow for movie data pipeline',
    schedule_interval='@weekly',  # Chạy thủ công hoặc định kỳ tùy chỉnh
    start_date=datetime(2024, 12, 1),
    catchup=False,
) as dag:

    # Task lấy dữ liệu phim từ API
    fetch_movie_data_task = BashOperator(
        task_id='fetch_movie_data',
        bash_command='python3 /opt/airflow/DE_project/ETL/extract/API_movie_Themoviedb.py',
    )

    # Task chuyển đổi dữ liệu phim từ JSON sang CSV
    movie_json_to_csv_task = BashOperator(
        task_id='movie_json_to_csv',
        bash_command='python3 /opt/airflow/DE_project/JSON_to_CSV/JSON_to_CSV_movie.py',
    )

    # Task lấy dữ liệu rating từ API
    fetch_rating_data_task = BashOperator(
        task_id='fetch_rating_data',
        bash_command='python3 /opt/airflow/DE_project/ETL/extract/API_rating_Themoviedb.py',
    )

    # Task chuyển đổi dữ liệu rating từ JSON sang CSV
    rating_json_to_csv_task = BashOperator(
        task_id='rating_json_to_csv',
        bash_command='python3 /opt/airflow/DE_project/JSON_to_CSV/JSON_to_CSV_rating.py',
    )

    # # Task transform dữ liệu movie
    transform_data_movie_task = BashOperator(
        task_id='transform_data_movie',
        bash_command='python3 /opt/airflow/DE_project/ETL/transform/transform_moviedf.py',
    )

    # Task transform dữ liệu rating
    transform_data_rating_task = BashOperator(
        task_id='transform_data_rating',
        bash_command='python3 /opt/airflow/DE_project/ETL/transform/transform_ratingdf.py',
    )
 
    # Task load dữ liệu movie vào data warehouse
    load_movie_to_dw_task = BashOperator(
        task_id='load_movive_to_dw',
        bash_command='python3 /opt/airflow/DE_project/ETL/load/load_moviedf_to_dw.py',
    )

    # Task load dữ liệu movie vào data warehouse
    load_rating_to_dw_task = BashOperator(
        task_id='load_rating_to_dw',
        bash_command='python3 /opt/airflow/DE_project/ETL/load/load_ratingdf_to_dw.py',
    )

    # Xác định thứ tự các task và Chuyển đổi dữ liệu phim và rating trước khi thực hiện transform và Load dữ liệu vào data warehouse
    fetch_movie_data_task >> movie_json_to_csv_task >> transform_data_movie_task >> load_movie_to_dw_task
    fetch_rating_data_task >> rating_json_to_csv_task >> transform_data_rating_task >> load_rating_to_dw_task
