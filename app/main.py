from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Project": "FakeCheck"}


@app.get("/news/{news_id}")
def read_item(news_id: int, q: Union[str, None] = None):
    return {"news_id": news_id, "q": q}