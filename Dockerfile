# В качестве базового используем образ Docker с Uvicorn под управлением Gunicorn для высокопроизводительных
# веб-приложений FastAPI на Python 3.9 с автоматической настройкой производительности.
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Установим зависимости пакетов проекта
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Загружаем обученные модели nlp
# RUN spacy download ru_core_news_lg

# Переносим файлы проекта
COPY ./app app
