# В качестве базового используем образ Docker с Uvicorn под управлением Gunicorn для высокопроизводительных
# веб-приложений FastAPI на Python 3.9 с автоматической настройкой производительности.
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Настройка переменных окружения
ENV PORT 8080
ENV APP_MODULE app.api:app
ENV LOG_LEVEL debug
ENV WEB_CONCURRENCY 2

# Установим зависимости пакетов spaCy, DeepPavlov, TensorFlow, LaBSE, SentenceTransformers, Natasha, Dostoevsky
COPY ./requirements/nlp.txt ./requirements/nlp.txt
RUN pip install -r requirements/nlp.txt
RUN spacy download ru_core_news_lg

# Установим другие зависимости
COPY ./requirements/base.txt ./requirements/base.txt
RUN pip install -r requirements/base.txt

COPY .env /app/.env
COPY ./app /app/app

#
WORKDIR /code

#
COPY ./requirements.txt /app/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#
COPY ./app /app

#
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
