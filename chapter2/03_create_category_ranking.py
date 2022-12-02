from datetime import date
from pathlib import Path

from google.cloud import bigquery

DATASET_ID = "k_and_r"  # "raw_k_and_r" ではないことに注意
DESTINATION_TABLE_ID = "category_ranking"
SQL_PATH = Path(__file__).parent / "chapter2/02_ranking.sql"


def create_table_from_sql(
    sql_path: Path, table_id: str, target_date: date
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


# 実行部分
if __name__ == "__main__":
    create_table_from_sql(SQL_PATH, DESTINATION_TABLE_ID, date(2021, 12, 30))
