# 5章 データパイプライン・ワークフローエンジン ハンズオン

このディレクトリには，5章ハンズオンに登場するコードが格納されています

以下，ハンズオンに登場するコマンドなどを再掲します

## 5.4.3 他基盤との接続

Cloud composer 環境への Python パッケージのインストール

```console
$ gcloud composer environments update starterkit \
    --location asia-northeast1 \
    --update-pypi-package google-cloud-firestore>=2.4.0
```
