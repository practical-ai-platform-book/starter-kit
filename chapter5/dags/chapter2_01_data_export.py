import pendulum
from airflow import models
from airflow.operators.python_operator import PythonOperator
from google.cloud import bigquery, storage

DATASET_ID = "raw_k_and_r"
# ご自身の準備した GCS Bucket 名を記載してください
# BUCKET_ID = ...


def download_from_gcs(
    bucket_name: str, source_blob_name: str, destination_file_name: str
) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def upload_bq(filename: str, table_id: str) -> None:
    client = bigquery.Client()
    dataset_ref = client.dataset(DATASET_ID)
    table_ref = dataset_ref.table(table_id)

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
    )

    with open(filename, "rb") as source_file:
        job = client.load_table_from_file(
            source_file, table_ref, job_config=job_config
        )
    job.result()


with models.DAG(
    dag_id="data_uploader",
    start_date=pendulum.datetime(2022, 5, 8, tz="Asia/Tokyo"),
    schedule_interval="0 3 * * *",
) as dag:
    items_downloader = PythonOperator(
        task_id="items_downloader",
        python_callable=download_from_gcs,
        op_kwargs={
            "bucket_name": BUCKET_ID,
            "source_blob_name": "items.csv",
            "destination_file_name": "./items.csv",
        },
    )

    items_uploader = PythonOperator(
        task_id="items_uploader",
        python_callable=upload_bq,
        op_kwargs={
            "filename": "./items.csv",
            "table_id": "items",
        },
    )

    transactions_downloader = PythonOperator(
        task_id="transactions_downloader",
        python_callable=download_from_gcs,
        op_kwargs={
            "bucket_name": BUCKET_ID,
            "source_blob_name": "transactions.csv",
            "destination_file_name": "./transactions.csv",
        },
    )

    transactions_uploader = PythonOperator(
        task_id="transactions_uploader",
        python_callable=upload_bq,
        op_kwargs={
            "filename": "./transactions.csv",
            "table_id": "transactions",
        },
    )

    users_downloader = PythonOperator(
        task_id="users_downloader",
        python_callable=download_from_gcs,
        op_kwargs={
            "bucket_name": BUCKET_ID,
            "source_blob_name": "users.csv",
            "destination_file_name": "./users.csv",
        },
    )

    users_uploader = PythonOperator(
        task_id="users_uploader",
        python_callable=upload_bq,
        op_kwargs={
            "filename": "./users.csv",
            "table_id": "users",
        },
    )

    items_downloader >> items_uploader
    transactions_downloader >> transactions_uploader
    users_downloader >> users_uploader
