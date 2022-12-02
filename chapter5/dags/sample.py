import logging

import pendulum
from airflow import models
from airflow.operators import bash_operator, python_operator


def greeting() -> None:
    logging.info("Hello world!")


with models.DAG(
    dag_id="composer_sample_simple_greeting",
    start_date=pendulum.datetime(2022, 5, 8, tz="Asia/Tokyo"),
    schedule_interval="30 16 * * *",
) as dag:
    hello_python = python_operator.PythonOperator(
        task_id="hello",
        python_callable=greeting,
    )

    sleep_bash = bash_operator.BashOperator(
        task_id="sleep",
        bash_command="sleep 10",
    )

    goodbye_bash = bash_operator.BashOperator(
        task_id="bye",
        bash_command="echo Goodbye.",
    )

    [hello_python, sleep_bash] >> goodbye_bash
