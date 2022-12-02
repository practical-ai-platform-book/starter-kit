from datetime import date
from pathlib import Path

from google.cloud import bigquery, firestore

BASEDIR = Path(__file__).parent


def main(target_date: date, max_items: int) -> None:
    # BigQuery 上で購入済みアイテムを集計する
    bigquery_client = bigquery.Client()
    sql = (BASEDIR / "purchased.sql").read_text()
    cfg = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                name="target_date",
                value=target_date,
                type_=bigquery.enums.SqlParameterScalarTypes.DATE,
            ),
            bigquery.ScalarQueryParameter(
                name="max_items",
                value=max_items,
                type_=bigquery.enums.SqlParameterScalarTypes.INT64,
            ),
        ]
    )
    result = bigquery_client.query(sql, cfg).result()

    # 結果を Firestore に格納する
    firestore_client = firestore.Client()
    firestore_writer = firestore_client.bulk_writer()
    collection = firestore_client.collection("purchased_items")
    for row in result:
        doc = collection.document(row["user_id"])
        data = {k: v for k, v in row.items() if k != "user_id"}
        firestore_writer.set(doc, data)
    firestore_writer.close()


if __name__ == "__main__":
    main(target_date=date(2021, 1, 1), max_items=10)
