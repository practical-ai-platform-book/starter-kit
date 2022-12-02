from typing import List, Tuple

import pandas as pd

from .constants import WORDS_INPUT, WORDS_SUGGEST


def _parse_queries(queries: List[str]) -> Tuple[List[str], List[str]]:
    """クエリをパースして関心のある単語だけを取り出す"""
    qs_input, qs_suggest = [], []
    for query in queries:
        qs = query.split()
        if len(qs) == 0:
            continue
        elif len(qs) == 1:
            if qs[0] in WORDS_INPUT:
                qs_input.append(qs[0])
                qs_suggest.append("none")
        else:
            if qs[0] in WORDS_INPUT:
                qs_input.append(qs[0])
                if qs[1] in WORDS_SUGGEST:
                    qs_suggest.append(qs[1])
                else:
                    qs_suggest.append("none")
    return qs_input, qs_suggest


def create_cooccurrence(df: pd.DataFrame) -> pd.DataFrame:
    """文字列でアクセスできる共起行列を作成する"""
    qs_input, qs_suggest = _parse_queries(df["query"].to_numpy().tolist())
    df_cooccur = pd.DataFrame({"input": qs_input, "suggest": qs_suggest})
    return pd.crosstab(
        df_cooccur["suggest"], df_cooccur["input"], normalize="columns"
    )


def main() -> None:
    df = pd.read_csv("data/queries.csv")
    genders = ["male", "female", "none"]
    for gender in genders:
        df_cooccur = create_cooccurrence(df.query(f"gender == '{gender}'"))
        df_cooccur.to_csv(
            f"chapter7/online/suggest_model/cooccurences/{gender}.csv"
        )


if __name__ == "__main__":
    main()
