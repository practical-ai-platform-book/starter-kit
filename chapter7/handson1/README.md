# 7章 API 基盤の発展 ハンズオンその1: 複数の key-value 型 API を組合わせる

このディレクトリには，7章ハンズオンその1に登場するコードが格納されています

以下，ハンズオンに登場するコマンドなどを再掲します

なお，各コマンドは[リポジトリルート](../)から実行することを想定しています

## 7.2.1 key-value 型 API を作る（再訪）

Firestore へのデータ登録（本文中では省略されています）

```console
$ poetry run python chapter7/handson1/kv_job/main.py  
```

Cloud Run へのデプロイ（本文中では省略されています）

```console
$ gcloud run deploy purchased-items \
    --region=asia-northeast1 \
    --source=. \
    --command=gunicorn,chapter7.handson1.kv_api.main:app,--worker-class,uvicorn.workers.UvicornWorker \
    --no-allow-unauthenticated
```

Cloud Run 上の API への未認証のリクエスト（URL はご自身の環境のものに書き換えてください）

```console
$ curl -i --get \
    https://purchased-items-xxxxxxxxxx-an.a.run.app/purchased_items \
    --data-urlencode user_id=000007
```

Cloud Run 上の API への認証済みリクエスト（URL はご自身の環境のものに書き換えてください）

```console
$ curl -i --get \
    -H "authorization: Bearer $(gcloud auth print-identity-token)" \
    https://purchased-items-xxxxxxxxxx-an.a.run.app/purchased_items \
    --data-urlencode user_id=000007
```

## 7.2.2 集約 API を実装する

ローカル環境の API の起動（バックエンド API の URL はご自身の環境のものに書き換えてください）

```console
$ export API_URL_PURCHASEDITEMS=https://purchased-items-xxxxxxxxxx-an.a.run.app/purchased_items
$ export API_URL_RANKING=https://category-ranking-xxxxxxxxxx-an.a.run.app/ranking
$ export VALID_API_KEY=dummy
$ poetry run gunicorn chapter7.handson1.agg_api.main:app \
    --worker-class uvicorn.workers.UvicornWorker
```

ローカル環境の API へのリクエスト

```console
$ curl -i --get \
    -H 'authorization: Bearer dummy' \
    http://localhost:8000/recommend \
    --data-urlencode category_id=DIY用品 \
    --data-urlencode user_id=000008
```

## 7.2.3 Cloud Run にデプロイする

API キーの生成・Secret Manager への登録

```console
$ python -c \
    'import random; print("dataapikey_" + "".join(random.choices("0123456789abcdef", k=64)), end="")' \
    | gcloud secrets create recommend-api-api-key --data-file=-
```

Cloud Run からシークレットへのアクセス権付与

```console
$ SA="$(
    gcloud compute project-info describe --format='value(defaultServiceAccount)'                                                                                           
)"
$ gcloud secrets add-iam-policy-binding \
    recommend-api-api-key \
    --member="serviceAccount:$SA" \
    --role=roles/secretmanager.secretAccessor
```

Cloud Run へのデプロイ（本文中では省略されています）

```console
$ gcloud run deploy personalized-ranking \
    --region=asia-northeast1 \
    --source=. \
    --command=gunicorn,chapter7.handson1.agg_api.main:app,--worker-class,uvicorn.workers.UvicornWorker \
    --set-env-vars=API_URL_PURCHASEDITEMS=https://purchased-items-xxxxxxxxxx-an.a.run.app/purchased_items,API_URL_RANKING=https://category-ranking-xxxxxxxxxx-an.a.run.app/ranking \
    --set-secrets=VALID_API_KEY=recommend-api-api-key:1 \
    --allow-unauthenticated
```
