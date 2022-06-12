from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

description = """
FakeCheck API - сервис проверки новостей
 
## evaluate

GET, POST - Получить оценку достоверности новости по шкале от 1 до 100 баллов. \
100 баллов соответствует полному совпадению с публикацией в источнике из белого списка (whitelist) \
1 балл - недостоверная новость. Больше баллов получают новости, которые соответствуют первоисточнику с точки зрения \
семантики и тональности

## detailEvaluate

GET, POST - Получить все значения метрик, использованных при определении оценки достоверности новости

## whitelist

GET - Получить список доверенных источников (white list)
PUT - Добавить элемент в список доверенных источников
DELETE - Удалить элемент из списка доверенных источников

## news
GET - Получить список последних новостей

## similarNews
GET, POST - Получить список похожих новостей
"""

app = FastAPI(
    title="FakeCheck",
    description=description,
    version="0.0.1",
    contact={
        "name": "DST-OFF",
        "url": "https://_fake_check_.ru",
        "email": "dst.off@yandex.ru",
    },
    license_info={
        "name": "None",
        "url": "https://www.___.ru",
    },
)

tags_metadata = [
    {
        "name": "evaluate",
        "description": "GET, POST - Получить оценку достоверности новости по шкале от 1 до 100 баллов. \
100 баллов соответствует полному совпадению с публикацией в источнике из белого списка (whitelist) \
1 балл - недостоверная новость. Больше баллов получают новости, которые соответствуют первоисточнику с точки зрения \
семантики и тональности",
    },
    {
        "name": "detailEvaluate",
        "description": "GET, POST - Получить все значения метрик, использованных при определении оценки достоверности новости",
    },
    {
        "name": "whitelist",
        "description": "GET - Получить список доверенных источников (white list) \
ADD - Добавить элемент в список доверенных источников \
DELETE - Удалить элемент из списка доверенных источников",
    },
    {
        "name": "lastNews",
        "description": "GET - Получить список последних новостей",
    },
    {
        "name": "similarNews",
        "description": "GET, POST - Получить список похожих новостей",
    },
]


class News(BaseModel):
    date: Union[str, None] = None
    title: Union[str, None] = None
    text: str


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


@app.get("/whitelist", tags=["whitelist"])
async def white_list():
    return {"whitelist": ['mos.ru']}


@app.get("/lastNews", tags=["lastNews"])
def last_news():
    return {"text": "lastNews"}


@app.get("/similarNews", tags=["similarNews"])
def similar_news(sentence: Union[str, None] = None):
    return {"text": sentence}


@app.post("/similarNews", tags=["similarNews"])
def similar_news(news: News):
    return {"text": news}


@app.get("/", response_class=RedirectResponse)
def redirect_fastapi():
    return "/docs"
