from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime


def _t1(ti):
    ti.xcom_push(key="my_key", value=42)

    # if return it's automatically push to xcom with default key -> return_value
    # return 42


def _t2(ti):
    # in log
    print(ti.xcom_pull(key="my_key", task_ids="t1"))


def _branch(ti):
    value = ti.xcom_pull(key="my_key", task_ids="t1")
    if value == 42:
        # next task
        return "t2"
    return "t3"


with DAG(
    "xcom_dag",
    start_date=datetime(2022, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="t1", python_callable=_t1)

    # branch operator is for condition to decide which task to do next -> return task id
    # BranchPythonOperator allow to write condition and return task id of next task in python
    branch = BranchPythonOperator(task_id="branch", python_callable=_branch)

    t2 = PythonOperator(task_id="t2", python_callable=_t2)

    t3 = BashOperator(task_id="t3", bash_command="echo ''")

    t4 = BashOperator(
        task_id="t4",
        bash_command="echo ''",
        #   trigger_rule="all_success" this is default
        trigger_rule="none_failed_min_one_success",  # if all upstream none failed and atleast one success it will trigger
    )

    # default trigger rule  is all success but in this case t3 is skip and t3 is upstream of t4 so t4 is skip too no matter t2 is success because it need to all success so we need to change trigger rule
    # use list for condition branch
    t1 >> branch >> [t2, t3] >> t4
