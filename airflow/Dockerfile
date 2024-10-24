# Use the official Airflow image as the base
FROM apache/airflow:2.10.2

# Switch to the root user to install packages
USER root

# Install Miniconda
RUN apt-get update && apt-get install -y wget \
    && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh \
    && bash ~/miniconda.sh -b -p /opt/conda \
    && rm ~/miniconda.sh \
    && /opt/conda/bin/conda clean -ya

# Switch back to the airflow user
USER airflow

# Add Conda to PATH
ENV PATH=/opt/conda/bin:$PATH

# Copy the environment.yml file into the container
COPY env_nobuild.yml /opt/airflow/environment.yml

# Create a Conda environment using the environment.yml file
RUN conda env create -f /opt/airflow/environment.yml || { echo "Conda environment creation failed"; exit 1; } \
    && conda clean -afy

# Set the user and environment variables
ENV AIRFLOW_UID=50000

# Switch to the non-root user
USER airflow

# Activate the Conda environment and set it as the default
#RUN conda activate trade
SHELL ["conda", "run", "-n", "trade", "/bin/bash", "-c"]
# Replace 'your_environment_name' with the name specified in your environment.yml file.

RUN pip install urllib3

# Set the environment variable to match your setup
ENV AIRFLOW_UID=50000
ENV AIRFLOW__CORE__EXECUTOR=CeleryExecutor
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
ENV AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres/airflow
ENV AIRFLOW__CELERY__BROKER_URL=redis://:@redis:6379/0
ENV AIRFLOW__CORE__FERNET_KEY=''
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=false
ENV AIRFLOW__CORE__LOAD_EXAMPLES=false
ENV AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK=true
ENV AIRFLOW__WEBSERVER__BASE_URL=http://localhost:8080
ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=60
ENV AIRFLOW__CORE__DAG_FILE_PROCESSOR_TIMEOUT=300
ENV AIRFLOW__SCHEDULER__ZOMBIE_TASK_THRESHOLD=600
ENV AIRFLOW__SCHEDULER__TASK_QUEUED_TIMEOUT=300
ENV AIRFLOW__LOGGING__LOGGING_LEVEL=DEBUG
ENV AIRFLOW__LOGGING__CELERY_LOGGING_LEVEL=DEBUG
