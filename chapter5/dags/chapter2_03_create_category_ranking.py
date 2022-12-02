from datetime import date
from os import getenv
from pathlib import Path

import pendulum
from airflow import models
from airflow.operators.python_operator import PythonOperator
from google.cloud import bigquery

DATASET_ID = "k_and_r"  # “raw_k_and_r” ではないことに注意
DESTINATION_TABLE_ID = "category_ranking"
SQL_PATH = Path(getenv("DAGS_FOLDER")) / "chapter2_02_ranking.sql"


def create_table_from_sql(
    sql_path: Path,
    table_id: str,
    target_date: date,
) -> None:
    client = bigquery.Client()
    table_ref = client.dataset(DATASET_ID).table(table_id)
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                name="target_date",
                value=target_date,
                type_=bigquery.enums.SqlParameterScalarTypes.DATE,
            ),
        ],
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        destination=table_ref,
    )
    query = sql_path.read_text()
    job = client.query(query, job_config=job_config)
    job.result()  # 新しいテーブルの作成


with models.DAG(
    dag_id="create_ranking",
    start_date=pendulum.datetime(2022, 5, 8, tz="Asia/Tokyo"),
    schedule_interval="30 3 * * *",
) as dag:
    create_sales = PythonOperator(
        task_id="create_sales",
        python_callable=create_table_from_sql,
        op_kwargs={
            "sql_path": SQL_PATH,
            "table_id": DESTINATION_TABLE_ID,
            "target_date": date(2021, 12, 31),
        },
    )
