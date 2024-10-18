from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import os

# Define the base directory for paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_INGESTION_SCRIPT = os.path.join(BASE_DIR, '../scripts/data_ingestion/store_data.py')
DATA_VISUALIZATION_SCRIPT = os.path.join(BASE_DIR, '../scripts/data_visualization/visualize_data.py')
DBT_RUN_COMMAND = "cd ../transformations && dbt run --select stock_data_transformed"

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 18),  # Set to the desired start date
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'trade_buddy_dag',
    default_args=default_args,
    description='A simple DAG for the Trade Buddy project',
    schedule_interval='@daily',  # Set your desired schedule
)

# Task 1: Ingest Data
ingest_data = PythonOperator(
    task_id='ingest_data',
    python_callable=lambda: os.system(f'python {DATA_INGESTION_SCRIPT}'),
    dag=dag,
)

# Task 2: Transform Data
transform_data = BashOperator(
    task_id='transform_data',
    bash_command=DBT_RUN_COMMAND,
    dag=dag,
)

# Task 3: Visualize Data
visualize_data = BashOperator(
     task_id='visualize_data',
     bash_command=lambda: os.system(f'python {DATA_VISUALIZATION_SCRIPT}'),
     dag=dag,
 )

# Setting task dependencies
ingest_data >> transform_data >> visualize_data

