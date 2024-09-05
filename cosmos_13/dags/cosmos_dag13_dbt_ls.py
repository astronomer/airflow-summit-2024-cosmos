import logging
from datetime import datetime
from pathlib import Path

from cosmos import DbtDag, ProjectConfig, RenderConfig, TestBehavior, ProfileConfig, ExecutionConfig, LoadMode
from cosmos import __version__ as cosmos_version
from cosmos.profiles import GoogleCloudServiceAccountFileProfileMapping

jaffle_shop_path = Path("/usr/local/airflow/dbt/jaffle_shop")

profile_mapping = GoogleCloudServiceAccountFileProfileMapping(
    conn_id="gcp_profile_conn",
    profile_args={
        "project": "observability-sandbox-344122",
        "dataset": "cosmos_dag13",
        "threads": 2,
    },
)

profile_config = ProfileConfig(
    profile_name="airflow_db",
    target_name="bq",
    profile_mapping=profile_mapping,
)

execution_config = ExecutionConfig(
    dbt_executable_path=Path("/usr/local/airflow/dbt_venv/bin/dbt"),
)

operator_args = {"install_deps": True}

project_config = ProjectConfig(jaffle_shop_path)

render_config = RenderConfig(
    test_behavior=TestBehavior.AFTER_EACH,
    dbt_deps=True,
    load_method=LoadMode.DBT_LS,
)

if cosmos_version.startswith("1.3"):
    cosmos_dag13_dbt_ls = DbtDag(
        # dbt/cosmos-specific parameters
        project_config=ProjectConfig(jaffle_shop_path),
        render_config=render_config,
        profile_config=profile_config,
        execution_config=execution_config,
        # normal dag parameters
        schedule=None,
        start_date=datetime(2023, 1, 1),
        operator_args=operator_args,
        catchup=False,
        dag_id="cosmos_dag13_dbt_ls",
        tags=["cosmos_dag13"],
    )
else:
    logging.info(f"Skipping DAG cosmos_dag13_dbt_ls for cosmos version {cosmos_version}")
