from asyncio import create_task
from http import HTTPStatus
from os import environ
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from .apikey import validate_api_key
from .cloudrun_client import CloudRunClient

API_URL_RANKING = environ["API_URL_RANKING"]
API_URL_PURCHASEDITEMS = environ["API_URL_PURCHASEDITEMS"]


app = FastAPI()
client: CloudRunClient


@app.on_event("startup")
async def startup() -> None:
    global client
    client = CloudRunClient()


@app.on_event("shutdown")
async def shutdown() -> None:
    await client.close()


class RecommendResponse(BaseModel):
    item_ids: List[str]


@app.get("/recommend", response_model=RecommendResponse)
async def recommend(
    category_id: str, user_id: str, _: None = Depends(validate_api_key)
) -> RecommendResponse:
    # ランキング API と購入履歴 API を並列で呼ぶ
    call_ranking = create_task(
        client.get(API_URL_RANKING, params={"category_id": category_id})
    )
    call_purchaseditems = create_task(
        client.get(
            API_URL_PURCHASEDITEMS, params={"user_id": user_id}, need_auth=True
        )
    )
    status_ranking, body_ranking = await call_ranking
    status_purchaseditems, body_purchaseditems = await call_purchaseditems

    # ランキングAPIがエラーのときはエラーを返す
    if status_ranking != HTTPStatus.OK:
        raise HTTPException(
            status_code=status_ranking, detail="ranking api error"
        )
    items_base = body_ranking["items"]

    # 購入履歴APIがエラーのときはランキングをそのまま返す
    if status_purchaseditems != HTTPStatus.OK:
        return RecommendResponse(item_ids=items_base)
    items_purchased = set(body_purchaseditems["item_ids"])

    # items_base のうち，items_purchased に含まれないもののみ残す（元の順序は保つ）
    items = [item for item in items_base if item not in items_purchased]
    return RecommendResponse(item_ids=items)
