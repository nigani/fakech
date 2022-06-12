from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse


description = """
FakeCheck API - сервис проверки новостей
 
## evaluate

GET, POST - Получить оценку достоверности новости по шкале от 1 до 100 баллов. \
100 баллов соответствует полному совпадению с публикацией в источнике из белого списка (whitelist) \
1 балл - недостоверная новость. Больше баллов получают новости, которые соответствуют первоисточнику с точки зрения \
семантики и тональности

## еvaluate/detail

GET, POST - Получить все значения метрик, использованных при определении оценки достоверности новости

## whitelist

GET - Получить список доверенных источников (white list)
ADD - Добавить элемент в список доверенных источников
DELETE - Удалить элемент из списка доверенных источников

## news
GET - Получить список последних новостей

## news/similar
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
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "еvaluate/detail",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
    {
        "name": "whitelist",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
    {
        "name": "news",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
    {
        "name": "news/similar",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
]


@app.get("еvaluate", tags=["news"])
async def read_item(small_text: Union[str, None] = None):
    return {"text": small_text}


@app.get("еvaluate/detail", tags=["news"])
async def read_item(small_text: Union[str, None] = None):
    return {"text": small_text}


@app.get("whitelist", tags=["news"])
async def read_item():
    return {"whitelist": ['mos.ru']}


@app.get("/news/{small_text}", tags=["news"])
def read_item(small_text: Union[str, None] = None):
    return {"text": small_text}


@app.get("/", response_class=RedirectResponse)
def redirect_fastapi():
    return "/docs"
