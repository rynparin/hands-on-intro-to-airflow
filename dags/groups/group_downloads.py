from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup


def download_tasks():

    # We can put this block inside group_dag.py but separate make it's more clean
    with TaskGroup("downloads", tooltip="Download tasks") as group:
        download_a = BashOperator(task_id="download_a", bash_command="sleep 10")

        download_b = BashOperator(task_id="download_b", bash_command="sleep 10")

        download_c = BashOperator(task_id="download_c", bash_command="sleep 10")

        return group
