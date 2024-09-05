from datetime import datetime
from pathlib import Path

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from cosmos import DbtTaskGroup, ExecutionConfig, ExecutionMode, ProfileConfig, ProjectConfig
from cosmos.profiles import GoogleCloudServiceAccountFileProfileMapping

jaffle_shop_path = Path("/usr/local/airflow/dbt/jaffle_shop")

profile_mapping = GoogleCloudServiceAccountFileProfileMapping(
    conn_id="gcp_profile_conn",
    profile_args={
        "project": "observability-sandbox-344122",
        "dataset": "cosmos_dag16",
        "threads": 2,
    },
)

profile_config = ProfileConfig(
    profile_name="airflow_db",
    target_name="bq",
    profile_mapping=profile_mapping,
)

project_config = ProjectConfig(jaffle_shop_path)


# [START virtualenv_example]
@dag(
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
)
def example_virtualenv() -> None:
    start_task = EmptyOperator(task_id="start-venv-examples")
    end_task = EmptyOperator(task_id="end-venv-examples")

    # This first task group creates a new Cosmos virtualenv every time a task is run
    # and deletes it afterward.
    # It is much slower than if the user sets the `virtualenv_dir`
    tmp_venv_task_group = DbtTaskGroup(
        group_id="tmp-venv-group",
        project_config=ProjectConfig(jaffle_shop_path),
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            execution_mode=ExecutionMode.VIRTUALENV,
            # Without setting virtualenv_dir="/some/path/persistent-venv",
            # Cosmos creates a new Python virtualenv for each dbt task being executed
        ),
        operator_args={
            "py_system_site_packages": False,
            "py_requirements": ["dbt-bigquery"],
            "install_deps": True,
            "emit_datasets": False,  # Example of how to not set inlets and outlets
        },
    )

    # The following task group reuses the Cosmos-managed Python virtualenv across multiple tasks.
    # It runs approximately 70% faster than the previous TaskGroup.
    cached_venv_task_group = DbtTaskGroup(
        group_id="cached-venv-group",
        project_config=ProjectConfig(jaffle_shop_path),
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            execution_mode=ExecutionMode.VIRTUALENV,
            # We can set the argument `virtualenv_dir` if we want Cosmos to create one Python virtualenv
            # and reuse that to run all the dbt tasks within the same worker node
            virtualenv_dir=Path("/tmp/persistent-venv2"),
        ),
        operator_args={
            "py_system_site_packages": False,
            "py_requirements": ["dbt-bigquery"],
            "install_deps": True,
        },
    )

    start_task >> [tmp_venv_task_group, cached_venv_task_group] >> end_task


example_virtualenv()
# [END virtualenv_example]
