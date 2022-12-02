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


if __name__ == "__main__":
    main("k_and_r.category_ranking", "category_ranking", "category")
