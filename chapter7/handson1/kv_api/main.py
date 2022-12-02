from typing import List

from fastapi import FastAPI
from google.api_core.retry import Retry
from google.cloud.firestore import AsyncClient, DocumentSnapshot
from pydantic import BaseModel

app = FastAPI()
firestore = AsyncClient()

FIRESTORE_RETRY = Retry(
    initial=0.1,
    deadline=1.0,
)


class PurchasedItemsResponse(BaseModel):
    item_ids: List[str]


@app.get("/purchased_items", response_model=PurchasedItemsResponse)
async def purchased_items(user_id: str) -> PurchasedItemsResponse:
    doc_ref = firestore.collection("purchased_items").document(user_id)
    doc: DocumentSnapshot = await doc_ref.get(retry=FIRESTORE_RETRY)
    # NOTE: 存在しないユーザ（購入履歴のないユーザを含む）に対しては空リストを返す
    if not doc.exists:
        return PurchasedItemsResponse(item_ids=[])
    return PurchasedItemsResponse.parse_obj(doc.to_dict())
