from fastapi import FastAPI
from pydantic import BaseModel

from chapter7.online.suggest_model.model import SuggestModel

app = FastAPI()
model = SuggestModel()


class SuggestResponse(BaseModel):
    suggest: str


@app.get("/suggest", response_model=SuggestResponse)
async def Suggest(user_id: str, query: str) -> SuggestResponse:
    suggest = model(user_id, query)
    return SuggestResponse(suggest=suggest)
