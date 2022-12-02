# 2章 データの収集と蓄積 ハンズオン

このディレクトリには，2章ハンズオンに登場するコードが格納されています

以下，ハンズオンに登場するコマンドなどを再掲します

なお，各コマンドは[リポジトリルート](../)から実行することを想定しています

## 2.5.3 BigQuery にデータをアップロード（データを抽出・ためる）

CUI 経由でのアップロード

```console
$ bq load --skip_leading_rows=1 --source_format=CSV \
    raw_k_and_r.items data/items.csv \
    item_id:string,category:string
$ bq load --skip_leading_rows=1 --source_format=CSV \
    raw_k_and_r.transactions data/transactions.csv \
    date:date,user_id:string,item_id:string
$ bq load --skip_leading_rows=1 --source_format=CSV \
    raw_k_and_r.users data/users.csv \
    user_id:string,gender:string,birthday:string
```

コード経由でのアップロード（本書では `python3` で実行されていますが `poetry run python` と読み替えてください）

```console
$ poetry run python chapter2/01_data_export.py
```

## 2.5.4 売上げランキングマートの作成

CUI 経由での SQL 実行とテーブル保存

```console
$ bq query --use_legacy_sql=false \
    --destination_table=k_and_r.category_ranking \
    < chapter2/02_ranking.sql
```

コード経由での SQL 実行とテーブル保存（本書では `python3` で実行されていますが `poetry run python` と読み替えてください）

```console
$ poetry run python chapter2/03_create_category_ranking.py
```

## 2.5.5 テーブル連携の自動化

crontab に記載する内容

```
00 07 * * * poetry run python chapter2/01_data_export.py
30 07 * * * poetry run python chapter2/03_create_category_ranking.py
```
