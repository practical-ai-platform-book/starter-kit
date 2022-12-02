from pathlib import Path
from typing import Dict

import pandas as pd
from google.cloud import bigquery, firestore

from .constants import WORDS_INPUT, WORDS_SUGGEST

BASEDIR = Path(__file__).parent


class SuggestModel:
    def __init__(self, thres: float = 0.2) -> None:
        self.user_contexts_ref = firestore.Client().collection("search_context")
        self.user2gender = self._load_user2gender()
        self.dfs = self._load_dfs()
        self.thres = thres

    def __call__(self, user_id: str, query: str) -> str:
        """ユーザIDと入力単語に応じて，コンテキストの登録または単語サジェストのいずれかを行う"""
        qs = query.split()
        if len(qs) == 0:
            return ""
        elif len(qs) == 1:
            return self._suggest(user_id, qs[0])
        else:
            self._set_context(user_id, qs[1])
            return ""

    def _load_user2gender(self) -> Dict[str, str]:
        client = bigquery.Client()
        sql = (BASEDIR / "user_features.sql").read_text()
        df = client.query(sql).result().to_dataframe()
        return dict(zip(df["user_id"], df["gender"]))

    def _load_dfs(self) -> Dict[str, pd.DataFrame]:
        dfs = {}
        for gender in ["male", "female", "none"]:
            df = pd.read_csv(
                f"chapter7/online/suggest_model/cooccurences/{gender}.csv",
                index_col="suggest",
            )
            dfs[gender] = df
        return dfs

    def _set_context(self, user_id: str, word_ctx: str) -> None:
        if word_ctx in WORDS_SUGGEST:
            self.user_contexts_ref.document(user_id).set({"genre": word_ctx})

    def _suggest(self, user_id: str, word_input: str) -> str:
        doc: firestore.DocumentSnapshot = self.user_contexts_ref.document(
            user_id
        ).get()
        if not doc.exists:
            return ""
        if word_input not in WORDS_INPUT:
            return ""

        gender = self.user2gender.get(user_id, "none")
        df = self.dfs[gender]
        word_ctx = doc.to_dict()["genre"]
        score = df[word_input][word_ctx]
        if score > self.thres:
            return word_ctx
        else:
            return ""
