# 6章 データレイクとデータウェアハウス ハンズオン

このディレクトリには，6章ハンズオンに登場するコードが格納されています

以下，ハンズオンに登場するコマンドなどを再掲します

## 6.5.2 BigQuery データセットの事前準備

データセットの作成

```console
$ bq mk raw_k_and_r_chap6
```

データセットの一覧表示

```console
$ bq ls
```

## 6.5.3 データレイクの作成

_※ 注: この節のコマンドは [`data/`](../data/) ディレクトリで実行する場合のものが記載されています．[リポジトリルート](../)から実行する場合，ファイルパスを適宜修正してください_

users, items テーブルの取り込み

```console
$ bq load \
    --replace \
    --skip_leading_rows 1 --source_format=CSV \
    raw_k_and_r_chap6.items raw_items.csv \
    item_id:string,category:string
$ bq load \
    --replace \
    --skip_leading_rows 1 --source_format=CSV \
    raw_k_and_r_chap6.users raw_users.csv \
    user_id:string,gender:string,birthdate:string
```

transactions テーブルの取り込み

```console
$ bq load \
    --replace \
    --skip_leading_rows 1 \
    --source_format=CSV \
    --time_partitioning_type DAY \
    --time_partitioning_field date \
    raw_k_and_r_chap6.transactions \
    raw_transactions.csv \
    transaction_id:string,event_type:string,date:date,user_id:string,item_id:string
```

transactions テーブルの2021年12月21日分のみの更新

```console
$ bq load \
    --replace \
    --skip_leading_rows 1 \
    --source_format=CSV \
    --time_partitioning_type DAY \
    --time_partitioning_field date \
    'raw_k_and_r_chap6.transactions$20211229' \
    raw_transactions.20211229.csv \
    transaction_id:string,event_type:string,date:date,user_id:string,item_id:string
```

## 6.5.5 データウェアハウスの作成

_※ 注: この節のコマンドは本ディレクトリ `chapter6/` で実行する場合のものが記載されています．[リポジトリルート](../)から実行する場合，ファイルパスを適宜修正してください_

transactions の作成

```console
$ cat dwh_transactions.sql \
    | bq query \
        --time_partitioning_type DAY --time_partitioning_field date \
        --parameter=target_date:date:2021-12-29 \
        --destination_table='k_and_r.transactions$20211229' \
        --replace \
        --nodry_run
```

items, users の作成

```console
$ cat dwh_items.sql \
    | bq query --destination_table='k_and_r.items' --replace --nodry_run
$ cat dwh_users.sql \
    | bq query --destination_table='k_and_r.users' --replace --nodry_run
```

transactions_combined の作成

```console
$ cat dwh_transactions_combined.sql \
    | bq query \
        --time_partitioning_type DAY --time_partitioning_field date \
        --parameter=target_date:date:2021-12-29 \
        --destination_table='k_and_r.transactions_combined$20211229' \
        --replace \
        --nodry_run
```
