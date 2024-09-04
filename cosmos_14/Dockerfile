FROM quay.io/astronomer/astro-runtime:11.10.0-python-3.11

RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-postgres==1.5.4 dbt-bigquery && deactivate

#ENV AIRFLOW__COSMOS__ENABLE_CACHE=False
ENV AIRFLOW__CORE__TEST_CONNECTION=Enabled

ENV OPENLINEAGE_DISABLED=True
