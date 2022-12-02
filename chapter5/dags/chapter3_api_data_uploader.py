import pendulum
from airflow import models
from airflow.operators.python_operator import PythonOperator
from google.cloud import bigquery, firestore


def main(bigquery_table: str, firestore_collection: str, key: str) -> None:
    bigquery_client = bigquery.Client()
    result = bigquery_client.query(f"select * from `{bigquery_table}`").result()

    firestore_client = firestore.Client()
    firestore_writer = firestore_client.bulk_writer()
    collection = firestore_client.collection(firestore_collection)
    for row in result:
        doc = collection.document(row[key])
        data = {k: v for k, v in row.items() if k != key}
        firestore_writer.set(doc, data)
    firestore_writer.close()


with models.DAG(
    dag_id="api_data_uploader",
    start_date=pendulum.datetime(2022, 5, 8, tz="Asia/Tokyo"),
    schedule_interval="0 4 * * *",
) as dag:
    api_uploader = PythonOperator(
        task_id="uploader",
        python_callable=main,
        op_kwargs={
            "bigquery_table": "k_and_r.category_ranking",
            "firestore_collection": "category_ranking",
            "key": "category",
        },
    )
