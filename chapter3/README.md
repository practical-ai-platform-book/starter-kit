# 3章 Web API 基盤 ハンズオン

このディレクトリには，3章ハンズオンに登場するコードが格納されています

以下，ハンズオンに登場するコマンドなどを再掲します

なお，各コマンドは[リポジトリルート](../)から実行することを想定しています

## 3.4.3 BigQuery 上の集計済みテーブルを Cloud Firestore に連携する

連携スクリプトの実行

```console
poetry run python chapter3/job/main.py  
```

## 3.4.4 API の実装を書く

ローカル環境の API の起動（お好みで `--reload` や `--worker=4` オプションなどをつけてください）

```console
$ poetry run gunicorn chapter3.api.main:app \
    --worker-class uvicorn.workers.UvicornWorker
```

ローカル環境の API へのリクエスト

```console
$ curl -i --get \
    http://localhost:8000/ranking \
    --data-urlencode category_id=DIY用品
```

ローカル環境のサンプルサイトの起動（起動する際のポートを変更するには，末尾のポート番号を書き換えて実行してください）

```console
$ poetry run python -m http.server -d chapter3/client/ 8080
```

## 3.4.5 Cloud Run にデプロイする

Cloud Run へのデプロイ

```console
$ gcloud run deploy category-ranking \
    --region=asia-northeast1 \
    --source=. \
    --command=gunicorn,chapter3.api.main:app,--worker-class,uvicorn.workers.UvicornWorker \
    --allow-unauthenticated
```

Cloud Run 上の API へのリクエスト（URL はご自身の環境のものに書き換えてください）

```console
$ curl -i --get \
    https://category-ranking-xxxxxxxxxx-an.a.run.app/ranking \
    --data-urlencode category_id=DIY用品
```

## 3.4.6 ログを分析用データベースに連携

Cloud Run のアクセスログに絞り込むフィルタリングクエリ

```
log_id("run.googleapis.com/requests")
```

## 3.4.7 ランキングの自動更新

crontab に記載する内容

```
00 08 * * * poetry run python chapter3/job/main.py
```
