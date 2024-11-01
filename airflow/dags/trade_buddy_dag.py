from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import os

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

# Function to run Python scripts
def run_script(script_path):
    os.system(f'python {script_path}')

# Task 1: Ingest Data
ingest_data = BashOperator(
    task_id='ingest_data',
    bash_command=f'cd /opt/airflow/scripts/data_ingestion && python store_data.py',
    dag=dag,
)

# Task 2: Transform Data
transform_data = BashOperator(
    task_id='transform_data',
    bash_command=f'cd /opt/airflow/transformations && dbt run --select stock_data_transformed',
    dag=dag,
)

# Task 3: Visualize Data
visualize_data = BashOperator(
     task_id='visualize_data',
     bash_command=f'cd /opt/airflow/scripts/data_visualization && python visualize_data.py',
     dag=dag,
 )

# Setting task dependencies
ingest_data >> transform_data >> visualize_data

