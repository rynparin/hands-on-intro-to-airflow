from airflow import DAG
from airflow.operators.bash import BashOperator
from groups.group_downloads import download_tasks
from groups.group_transforms import transform_tasks

from datetime import datetime

#  subdags complicated to group your task so it's deprecated -> use task group instead

with DAG(
    "group_dag",
    start_date=datetime(2022, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    args = {
        "start_date": dag.start_date,
        "schedule_interval": dag.schedule_interval,
        "catchup": dag.catchup,
    }

    # download_a = BashOperator(task_id="download_a", bash_command="sleep 10")

    # download_b = BashOperator(task_id="download_b", bash_command="sleep 10")

    # download_c = BashOperator(task_id="download_c", bash_command="sleep 10")

    downloads = download_tasks()

    check_files = BashOperator(task_id="check_files", bash_command="sleep 10")

    # transform_a = BashOperator(task_id="transform_a", bash_command="sleep 10")

    # transform_b = BashOperator(task_id="transform_b", bash_command="sleep 10")

    # transform_c = BashOperator(task_id="transform_c", bash_command="sleep 10")

    transforms = transform_tasks()

    # (
    #     [download_a, download_b, download_c]
    #     >> check_files
    #     >> [transform_a, transform_b, transform_c]
    # )

    downloads >> check_files >> transforms
