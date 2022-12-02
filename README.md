# [実践]データ活用システム開発ガイド スターターキット

このリポジトリは，[[実践]データ活用システム開発ガイド 10年使えるシステムへのスモールスタート](http://www.tkd-pbl.com/book/b616180.html)（東京化学同人）のハンズオンのソースコードです

## ハンズオンを動かすために

ハンズオンの実行環境を構築する手順は本文第1章に掲載されているので，そちらをご確認ください．ここでは，各ソフトウェアのバージョンとセットアップに必要なコマンド類を再掲するに留めます

なお本リポジトリと書籍でコードの実行方法に差分がある場合は，本リポジトリの実行方法を利用するようにしてください．例えば書籍では `python3` コマンドでコードを実行している箇所がありますが，本リポジトリでは `poetry run python` で実行しています

### 使用するソフトウェアとセットアップコマンド

| ソフトウェア | 用途 | 動作確認バージョン |
|:---|:---|:---|
| [Python](https://www.python.org/downloads/) | データの加工<br />API リソースの作成<br />ワークフローの作成 | 3.9.10 |
| [Poetry](https://python-poetry.org/docs/#installation) | Python パッケージの依存管理 | 1.1.12 |
| [git](https://git-scm.com/downloads) | コードのバージョン管理 | 2.25.1 |
| [gcloud](https://cloud.google.com/sdk/docs/install) | Google Cloud のリソース管理 | Google Cloud SDK: 376.0.0<br />bq: 2.0.74<br />gsutil: 5.6 |

Python の依存関係セットアップ

```console
$ poetry install
```

gcloud 初期化

```console
$ gcloud init
```

gcloud 設定の確認

```console
$ gcloud auth list
$ gcloud config get core/project
```

gcloud 再ログイン・設定

```console
$ gcloud auth login
$ gcloud config set core/project $YOUR_PROJECT_ID
```

gcloud Python SDK 設定

```console
$ gcloud auth application-default login
$ export GOOGLE_CLOUD_PROJECT="$(gcloud config get core/project)"
```
