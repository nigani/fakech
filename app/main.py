from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

from app.tools import *

description = """
FakeCheck API - сервис проверки новостей
 
## whitelist

GET - Получить список доверенных источников (white list)
PUT - Добавить элемент в список доверенных источников (в разработке)
DELETE - Удалить элемент из списка доверенных источников (в разработке)

## lastNews
GET - Получить список последних новостей

## evaluate

GET, POST - Получить оценку достоверности новости по шкале от 1 до 100 баллов. \
100 баллов соответствует полному совпадению с публикацией в источнике из белого списка (whitelist) \
1 балл - недостоверная новость. Больше баллов получают новости, которые соответствуют первоисточнику с точки зрения \
семантики и тональности

## detailEvaluate

GET, POST - Получить все значения метрик, использованных при определении оценки достоверности новости

## similarNews
GET, POST - Получить список похожих новостей
"""

tags_metadata = [
    {
        "name": "whitelist",
        "description": "GET - Получить список доверенных источников (white list)\n"
                       "ADD - Добавить элемент в список доверенных источников \n"
                       "DELETE - Удалить элемент из списка доверенных источников",
    },
    {
        "name": "lastNews",
        "description": "GET - Получить список последних новостей",
    },
    {
        "name": "evaluate",
        "description": "GET, POST - Получить оценку достоверности новости по шкале от 1 до 100 баллов. \n"
                       "100 баллов соответствует полному совпадению с публикацией в источнике из белого списка "
                       "(whitelist) \n 1 балл - недостоверная новость. Больше баллов получают новости, которые "
                       "соответствуют первоисточнику с точки зрения семантики и тональности",
    },
    {
        "name": "detailEvaluate",
        "description":
            "GET, POST - Получить все значения метрик, использованных при определении оценки достоверности новости",
    },
    {
        "name": "similarNews",
        "description": "GET, POST - Получить список похожих новостей",
    },
]

app = FastAPI(
    title="FakeCheck",
    description=description,
    version="0.0.1",
    contact={
        "name": "DST-OFF",
        "url": "https://github.com/nigani/fakech",
        "email": "dst.off@yandex.ru",
    },
)


class News(BaseModel):
    date: Union[str, None] = None
    title: Union[str, None] = None
    text: str


@app.get("/whitelist", tags=["whitelist"])
def white_list():
    return {"whitelist": ['mos.ru']}


@app.get("/lastNews", tags=["lastNews"])
def last_news():
    print("/lastNews")
    return {"lastNews": news_load()}


@app.get("/similarNews", tags=["similarNews"])
def similar_news(sentence: Union[str, None] = None):
    print("/lastNews")
    return {"text": sentence}


@app.post("/similarNews", tags=["similarNews"])
def similar_news(news: News):
    return {"text": news}


@app.get("/evaluate", tags=["evaluate"])
async def evaluate(sentence: Union[str, None] = None):
    return {"text": sentence}


@app.post("/evaluate", tags=["evaluate"])
async def evaluate(news: News):
    return {"text": news}


@app.get("/detailEvaluate", tags=["detailEvaluate"])
async def detail_evavuate(sentence: Union[str, None] = None):
    return {"text": sentence}


@app.post("/detailEvaluate", tags=["detailEvaluate"])
async def detail_evavuate(news: News):
    return {"text": news}


@app.get("/", response_class=RedirectResponse)
def redirect_fastapi():
    return "/docs"
