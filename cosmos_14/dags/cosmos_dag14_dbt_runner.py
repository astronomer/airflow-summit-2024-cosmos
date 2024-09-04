from datetime import datetime
from pathlib import Path

from cosmos import DbtDag, ProjectConfig, RenderConfig, TestBehavior, ProfileConfig, ExecutionConfig, LoadMode
from cosmos import __version__ as cosmos_version
from cosmos.config import InvocationMode


import logging

jaffle_shop_path = Path("/usr/local/airflow/dbt/jaffle_shop")

profile_config = ProfileConfig(
    # these map to dbt/jaffle_shop/profiles.yml
    profile_name="airflow_db",
    target_name="bq",
    profiles_yml_filepath=jaffle_shop_path / "profiles.yml",
)

execution_config = ExecutionConfig(
    invocation_mode=InvocationMode.DBT_RUNNER
)

operator_args = {"install_deps": True}

project_config = ProjectConfig(jaffle_shop_path)

render_config = RenderConfig(
    test_behavior=TestBehavior.AFTER_EACH,
    dbt_deps=True,
    load_method=LoadMode.DBT_LS,
)

if cosmos_version.startswith("1.4"):
    cosmos_dag14_dbt_runner = DbtDag(
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
        dag_id="cosmos_dag14_dbt_runner",
        tags=["cosmos_dag14"],
    )
else:
    logging.info(f"Skipping DAG cosmos_dag14 for cosmos version {cosmos_version}")
