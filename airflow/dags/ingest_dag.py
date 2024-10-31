from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import os

# Define the base directory for paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
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
    'ingest_dag',
    default_args=default_args,
    description='A simple DAG for the Trade Buddy project',
    schedule_interval='@daily',  # Set your desired schedule
)

# Function to run Python scripts
def run_script(script_path):
    os.system(f'python {script_path}')

# test: Transform Data
test1 = BashOperator(
    task_id='test1',
    bash_command=f'cd /opt/airflow/scripts/data_ingestion && python store_data.py',
    dag=dag,
)

# Task 1: Ingest Data
ingest_data = PythonOperator(
    task_id='ingest_data',
    python_callable=run_script,
    op_kwargs={'script_path': DATA_INGESTION_SCRIPT},  # Pass the script path as an argument
    dag=dag,
)

# Setting task dependencies
ingest_data  
