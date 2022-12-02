# 7章 API 基盤の発展 ハンズオンその2: オンライン推論 API を作る

このディレクトリには，7章ハンズオンその2に登場するコードが格納されています

以下，ハンズオンに登場するコマンドなどを再掲します

なお，各コマンドは[リポジトリルート](../)から実行することを想定しています

## 7.3.3 共起確率を集計する

共起確率データファイル `suggest_model/cooccurences/*.csv` の作成（本文中では省略されています）

```console
$ poetry run python chapter7/handson2/suggest_model/train.py
```

## 7.3.4 API の実装を書く

ローカル環境の API の起動（お好みで `--reload` や `--worker=4` オプションなどをつけてください）

```console
$ poetry run gunicorn chapter7.handson2.main:app \
    --worker-class uvicorn.workers.UvicornWorker
```

ローカル環境の API へのリクエスト

```console
$ # 初回のリクエストで，ユーザ000000はメンズ商品を検索しているとわかる
$ curl -i --get http://127.0.0.1:8000/suggest \
    --data-urlencode user_id=000000 \
    --data-urlencode query="Tシャツ メンズ"
HTTP/1.1 200 OK
date: Sat, 23 Apr 2022 10:45:03 GMT
server: uvicorn
content-length: 14
content-type: application/json

{"suggest":""}

$ # 以降で服を検索しているときは「メンズ」のクエリをサジェストする
$ curl -i --get http://127.0.0.1:8000/suggest \
    --data-urlencode user_id=000000 \
    --data-urlencode query="ポロシャツ"
HTTP/1.1 200 OK
date: Sat, 23 Apr 2022 10:45:48 GMT
server: uvicorn
content-length: 23
content-type: application/json

{"suggest":"メンズ"}

$ # 服以外を検索しているときにはサジェストを行わない
$ curl -i --get http://127.0.0.1:8000/suggest \
    --data-urlencode user_id=000000 \
    --data-urlencode query="コーヒー"
HTTP/1.1 200 OK
date: Sat, 23 Apr 2022 10:46:14 GMT
server: uvicorn
content-length: 14
content-type: application/json

{"suggest":""}
```

## 7.3.5 Cloud Run にデプロイする

Cloud Run へのデプロイ（本文中では省略されています）

```console
$ gcloud run deploy search-suggest \
    --region=asia-northeast1 \
    --source=. \
    --command=gunicorn,chapter7.handson2.main:app,--worker-class,uvicorn.workers.UvicornWorker \
    --allow-unauthenticated
```
