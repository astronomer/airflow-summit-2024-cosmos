FROM quay.io/astronomer/astro-runtime:11.10.0-python-3.11

RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-postgres==1.5.4 dbt-bigquery && deactivate

ENV AIRFLOW__CORE__TEST_CONNECTION=Enabled

ENV OPENLINEAGE_DISABLED=True

ENV AIRFLOW__COSMOS__REMOTE_CACHE_DIR="s3://cosmos-remote-cache/cosmos/"
ENV AIRFLOW__COSMOS__REMOTE_CACHE_DIR_CONN_ID="aws_s3_conn"
