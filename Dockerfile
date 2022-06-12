# В качестве базового используем образ Docker с Uvicorn под управлением Gunicorn для высокопроизводительных
# веб-приложений FastAPI на Python 3.9 с автоматической настройкой производительности.
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Установим зависимости пакетов проекта
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Загружаем обученные модели nlp
# RUN spacy download ru_core_news_lg

# Переносим файлы проекта
COPY ./app app

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
