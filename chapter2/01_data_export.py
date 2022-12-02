from google.cloud import bigquery

DATASET_ID = "raw_k_and_r"  # please create before running this code

# ローカルファイルからBigQueryのテーブルを作成
def upload_bq(filename: str, table_id: str) -> None:
    client = bigquery.Client()

    dataset_ref = client.dataset(DATASET_ID)
    table_ref = dataset_ref.table(table_id)

    job_config = bigquery.LoadJobConfig(
        autodetect=True,  # スキーマを自動検出
        source_format=bigquery.SourceFormat.CSV,  # ファイルのフォーマット指定
        skip_leading_rows=1,  # ヘッダーを除外
    )

    with open(filename, "rb") as source_file:
        job = client.load_table_from_file(
            source_file, table_ref, job_config=job_config
        )  # 読み込みジョブの作成
        job.result()  # ジョブの実行＝アップロード


# 実行部分
if __name__ == "__main__":
    upload_bq("./data/items.csv", "items")
    upload_bq("./data/transactions.csv", "transactions")
    upload_bq("./data/users.csv", "users")
