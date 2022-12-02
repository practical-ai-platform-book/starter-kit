from http import HTTPStatus
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.api_core.retry import Retry
from google.cloud.firestore import AsyncClient, DocumentSnapshot
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
)

firestore = AsyncClient()
FIRESTORE_RETRY = Retry(
    initial=0.1,
    deadline=1.0,
)


class RankingResponse(BaseModel):
    items: List[str]


@app.get("/ranking", response_model=RankingResponse)
async def ranking(category_id: str) -> RankingResponse:
    doc_ref = firestore.collection("category_ranking").document(category_id)
    doc: DocumentSnapshot = await doc_ref.get(retry=FIRESTORE_RETRY)
    if not doc.exists:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="specified category not found",
        )
    return RankingResponse.parse_obj(doc.to_dict())
